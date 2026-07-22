#!/usr/bin/env python3
"""Pre-hardware TVC gimbal response simulation.

Model:
    I theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance

The servo is represented as a first-order actuator lag plus command saturation.
This is intentionally low-order: the goal is to create a prediction baseline
that can be updated after the first hardware logs arrive.
"""

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class AxisPlant:
    name: str
    inertia_kg_m2: float
    damping_nms_per_rad: float
    stiffness_nm_per_rad: float
    servo_time_constant_s: float
    servo_torque_per_rad: float
    torque_limit_nm: float
    gravity_bias_nm: float


PITCH = AxisPlant(
    name="pitch",
    inertia_kg_m2=3.0e-5,
    damping_nms_per_rad=5.0e-4,
    stiffness_nm_per_rad=1.8e-2,
    servo_time_constant_s=0.055,
    servo_torque_per_rad=1.2,
    torque_limit_nm=0.13,
    gravity_bias_nm=0.018,
)

YAW = AxisPlant(
    name="yaw",
    inertia_kg_m2=3.0e-4,
    damping_nms_per_rad=2.0e-3,
    stiffness_nm_per_rad=3.9e-2,
    servo_time_constant_s=0.070,
    servo_torque_per_rad=1.4,
    torque_limit_nm=0.13,
    gravity_bias_nm=0.039,
)


def clamp(value, low, high):
    return max(low, min(high, value))


def command_deg(t_s, amplitude_deg=5.0, step_time_s=0.5):
    return 0.0 if t_s < step_time_s else amplitude_deg


def simulate(axis: AxisPlant, duration_s=4.0, dt_s=0.002, amplitude_deg=5.0):
    theta = 0.0
    omega = 0.0
    actuator_angle = 0.0
    rows = []
    n = int(duration_s / dt_s) + 1

    for i in range(n):
        t_s = i * dt_s
        cmd = math.radians(command_deg(t_s, amplitude_deg))

        # First-order actuator dynamics: delta_dot = (cmd - delta)/tau.
        actuator_angle += dt_s * (cmd - actuator_angle) / axis.servo_time_constant_s

        torque_cmd = axis.servo_torque_per_rad * (actuator_angle - theta)
        torque_cmd = clamp(torque_cmd, -axis.torque_limit_nm, axis.torque_limit_nm)

        # Gravity/cable bias is modeled as an approximately constant disturbance.
        tau_dist = axis.gravity_bias_nm
        theta_ddot = (
            torque_cmd
            + tau_dist
            - axis.damping_nms_per_rad * omega
            - axis.stiffness_nm_per_rad * theta
        ) / axis.inertia_kg_m2

        omega += dt_s * theta_ddot
        theta += dt_s * omega

        theta_deg = math.degrees(theta)
        omega_dps = math.degrees(omega)
        cmd_deg = math.degrees(cmd)
        pwm_us = int(round(1500 + 20.0 * cmd_deg))
        rows.append({
            "time_ms": int(round(t_s * 1000)),
            "mode": f"prehardware_{axis.name}_step",
            f"{axis.name}_cmd_deg": cmd_deg,
            f"meas_{axis.name}_deg": theta_deg,
            f"{axis.name}_pwm_us": pwm_us,
            f"gyro_{axis.name}_dps": omega_dps,
            "servo_angle_deg": math.degrees(actuator_angle),
            "servo_torque_nm": torque_cmd,
            "disturbance_torque_nm": tau_dist,
        })
    return rows


def write_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--axis", choices=("pitch", "yaw", "both"), default="both")
    parser.add_argument("--outdir", type=Path, default=Path("data/examples"))
    args = parser.parse_args()

    selected = []
    if args.axis in ("pitch", "both"):
        selected.append(PITCH)
    if args.axis in ("yaw", "both"):
        selected.append(YAW)

    args.outdir.mkdir(parents=True, exist_ok=True)
    model_path = args.outdir / "prehardware_model_parameters.json"
    model_path.write_text(json.dumps([asdict(axis) for axis in selected], indent=2) + "\n")
    print(f"Wrote {model_path}")

    for axis in selected:
        rows = simulate(axis)
        path = args.outdir / f"prehardware_{axis.name}_step_prediction.csv"
        write_csv(rows, path)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
