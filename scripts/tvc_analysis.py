"""Analysis utilities for two-axis TVC bench-test CSV logs."""

from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass
class StepMetrics:
    axis: str
    samples: int
    step_start_s: float
    initial_command_deg: float
    final_command_deg: float
    step_amplitude_deg: float
    response_delay_s: Optional[float]
    rise_time_10_90_s: Optional[float]
    settling_time_2pct_s: Optional[float]
    overshoot_pct: float
    steady_state_error_deg: float
    peak_abs_error_deg: float
    hysteresis_bias_deg: Optional[float]


def load_csv(path: str | Path) -> List[dict]:
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(line for line in f if not line.startswith("#"))
        return list(reader)


def _float(row: dict, key: str, default: float = 0.0) -> float:
    value = row.get(key, "")
    if value in ("", None):
        return default
    return float(value)


def get_time_s(rows: Iterable[dict]) -> List[float]:
    rows = list(rows)
    if not rows:
        return []
    if "time_s" in rows[0]:
        return [_float(r, "time_s") for r in rows]
    return [_float(r, "time_ms") / 1000.0 for r in rows]


def get_command(rows: Iterable[dict], axis: str) -> List[float]:
    key = f"{axis}_cmd_deg"
    alt_key = f"cmd_{axis}_deg"
    return [_float(r, key if key in r else alt_key) for r in rows]


def get_measured(rows: Iterable[dict], axis: str) -> List[float]:
    key = f"meas_{axis}_deg"
    if rows and key in rows[0]:
        return [_float(r, key) for r in rows]
    return _estimate_angle_from_quaternion(rows, axis)


def _estimate_angle_from_quaternion(rows: Iterable[dict], axis: str) -> List[float]:
    angles = []
    for row in rows:
        qw = _float(row, "quat_w", 1.0)
        qx = _float(row, "quat_x", 0.0)
        qy = _float(row, "quat_y", 0.0)
        qz = _float(row, "quat_z", 0.0)

        # Aerospace 3-2-1 style pitch/yaw extraction for small-angle analysis.
        sin_pitch = 2.0 * (qw * qy - qz * qx)
        sin_pitch = max(-1.0, min(1.0, sin_pitch))
        pitch = math.degrees(math.asin(sin_pitch))

        yaw = math.degrees(math.atan2(
            2.0 * (qw * qz + qx * qy),
            1.0 - 2.0 * (qy * qy + qz * qz),
        ))
        angles.append(pitch if axis == "pitch" else yaw)
    return angles


def analyze_step_response(rows: List[dict], axis: str = "pitch") -> StepMetrics:
    if len(rows) < 5:
        raise ValueError("Need at least five samples for step-response analysis.")

    t = get_time_s(rows)
    cmd = get_command(rows, axis)
    meas = get_measured(rows, axis)

    step_idx = _find_step_index(cmd)
    initial_cmd = _mean(cmd[:step_idx])
    final_cmd = _mean(cmd[max(step_idx, len(cmd) - max(3, len(cmd) // 5)):])
    amp = final_cmd - initial_cmd
    if abs(amp) < 1e-9:
        raise ValueError("No command step detected.")

    initial_meas = _mean(meas[:step_idx])
    final_meas = _mean(meas[max(step_idx, len(meas) - max(3, len(meas) // 5)):])
    target_delta = final_meas - initial_meas
    sign = 1.0 if amp >= 0.0 else -1.0

    t0 = t[step_idx]
    delay = _first_crossing_time(t, meas, step_idx, initial_meas + 0.02 * target_delta, sign)
    t10 = _first_crossing_time(t, meas, step_idx, initial_meas + 0.10 * target_delta, sign)
    t90 = _first_crossing_time(t, meas, step_idx, initial_meas + 0.90 * target_delta, sign)
    rise_time = None if t10 is None or t90 is None else max(0.0, t90 - t10)

    settling_time = _settling_time(t, meas, step_idx, final_meas, abs(0.02 * amp))
    peak_meas = max(meas[step_idx:]) if sign > 0 else min(meas[step_idx:])
    overshoot = max(0.0, sign * (peak_meas - final_meas))
    overshoot_pct = 100.0 * overshoot / max(abs(amp), 1e-9)

    errors = [c - y for c, y in zip(cmd, meas)]
    steady_error = _mean(errors[-max(3, len(errors) // 5):])
    peak_abs_error = max(abs(e) for e in errors)
    hysteresis_bias = _hysteresis_bias(cmd, meas)

    return StepMetrics(
        axis=axis,
        samples=len(rows),
        step_start_s=t0,
        initial_command_deg=initial_cmd,
        final_command_deg=final_cmd,
        step_amplitude_deg=amp,
        response_delay_s=None if delay is None else delay - t0,
        rise_time_10_90_s=rise_time,
        settling_time_2pct_s=None if settling_time is None else settling_time - t0,
        overshoot_pct=overshoot_pct,
        steady_state_error_deg=steady_error,
        peak_abs_error_deg=peak_abs_error,
        hysteresis_bias_deg=hysteresis_bias,
    )


def save_metrics(metrics: StepMetrics, path: str | Path) -> None:
    Path(path).write_text(json.dumps(asdict(metrics), indent=2) + "\n")


def _find_step_index(cmd: List[float]) -> int:
    deltas = [abs(cmd[i] - cmd[i - 1]) for i in range(1, len(cmd))]
    if not deltas:
        return 1
    return deltas.index(max(deltas)) + 1


def _mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _first_crossing_time(t, y, start_idx, threshold, sign):
    for i in range(start_idx, len(y)):
        if sign * (y[i] - threshold) >= 0.0:
            return t[i]
    return None


def _settling_time(t, y, start_idx, final_value, band):
    for i in range(start_idx, len(y)):
        if all(abs(v - final_value) <= band for v in y[i:]):
            return t[i]
    return None


def _hysteresis_bias(cmd: List[float], meas: List[float]) -> Optional[float]:
    positive = [y for c, y in zip(cmd, meas) if c > 0.5 * max(cmd)]
    negative = [y for c, y in zip(cmd, meas) if c < 0.5 * min(cmd)]
    if len(positive) < 3 or len(negative) < 3:
        return None
    return 0.5 * (_mean(positive[-len(positive)//2:]) + _mean(negative[-len(negative)//2:]))
