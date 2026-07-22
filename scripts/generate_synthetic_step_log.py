#!/usr/bin/env python3
"""Generate a synthetic Rev A step-response log.

This lets the analysis pipeline be tested before hardware is connected.
"""

import argparse
import csv
import math
from pathlib import Path


FIELDS = [
    "time_ms",
    "mode",
    "pitch_cmd_deg",
    "yaw_cmd_deg",
    "pitch_pwm_us",
    "yaw_pwm_us",
    "meas_pitch_deg",
    "meas_yaw_deg",
    "imu_present",
    "quat_w",
    "quat_x",
    "quat_y",
    "quat_z",
    "gyro_x_dps",
    "gyro_y_dps",
    "gyro_z_dps",
]


def synthetic_response(t_s, cmd_deg):
    """Second-order-looking response with lag, overshoot, and small bias."""
    if t_s < 1.0:
        return 0.05 * math.sin(2.0 * math.pi * t_s)
    tau = t_s - 1.0
    wn = 11.0
    zeta = 0.48
    wd = wn * math.sqrt(1.0 - zeta * zeta)
    response = 1.0 - math.exp(-zeta * wn * tau) * (
        math.cos(wd * tau) + zeta / math.sqrt(1.0 - zeta * zeta) * math.sin(wd * tau)
    )
    bias = 0.18
    return cmd_deg * response + bias


def quat_from_pitch_deg(pitch_deg):
    half = math.radians(pitch_deg) / 2.0
    return math.cos(half), 0.0, math.sin(half), 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("data/examples/synthetic_pitch_step.csv"))
    parser.add_argument("--duration", type=float, default=5.0)
    parser.add_argument("--hz", type=float, default=50.0)
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    dt = 1.0 / args.hz
    cmd_deg = 5.0
    prev_meas = 0.0

    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()

        n = int(args.duration * args.hz) + 1
        for i in range(n):
            t_s = i * dt
            cmd = 0.0 if t_s < 1.0 else cmd_deg
            meas = synthetic_response(t_s, cmd_deg)
            gyro_y = (meas - prev_meas) / dt
            prev_meas = meas
            qw, qx, qy, qz = quat_from_pitch_deg(meas)

            writer.writerow({
                "time_ms": int(round(t_s * 1000.0)),
                "mode": "synthetic_step_pitch",
                "pitch_cmd_deg": cmd,
                "yaw_cmd_deg": 0.0,
                "pitch_pwm_us": int(round(1500 + 20 * cmd)),
                "yaw_pwm_us": 1500,
                "meas_pitch_deg": meas,
                "meas_yaw_deg": 0.0,
                "imu_present": 1,
                "quat_w": qw,
                "quat_x": qx,
                "quat_y": qy,
                "quat_z": qz,
                "gyro_x_dps": 0.0,
                "gyro_y_dps": gyro_y,
                "gyro_z_dps": 0.0,
            })

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
