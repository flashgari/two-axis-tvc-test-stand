# Firmware Bring-Up Plan

## Objective

Bring up the Pico controller without risking servo or gimbal damage. The firmware sequence intentionally starts open-loop because the physical plant must be characterized before closed-loop control claims are meaningful.

## Embedded Control Chain

The first controller stack is:

```text
test mode -> commanded angle -> safety clamp -> PWM pulse width -> servo -> gimbal motion -> IMU/telemetry
```

The current firmware implements the first half of that chain:

- command profiles
- `+/-10 deg` angle clamp
- angle-to-PWM conversion
- servo neutral/sweep/step commands
- BNO085 detection placeholder
- CSV telemetry

## Why Open-Loop Comes Before PID

The rotational plant is:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The controller cannot be tuned intelligently until the physical terms are observed:

| Physical effect | Where it appears in data |
| --- | --- |
| servo speed limit | rise time and phase lag |
| gear backlash | different output angle depending on approach direction |
| deadband | small PWM changes produce no motion |
| frame compliance | slow settling or elastic rebound |
| wire preload | steady-state bias or asymmetric response |
| sensor filtering | delayed or smoothed attitude/rate telemetry |

Open-loop step and sweep tests identify these effects before a feedback loop tries to hide them.

## Bring-Up Sequence

### 1. Pico Only

- Load MicroPython.
- Copy `firmware/src/*.py` onto the Pico.
- Keep `MODE = "neutral"`.
- Confirm USB serial prints CSV header and rows.

Expected result:

```text
pitch_cmd_deg = 0
yaw_cmd_deg = 0
pitch_pwm_us = 1500
yaw_pwm_us = 1500
```

### 2. Servo Signal Without Mechanical Load

- Connect one HS-625MG signal wire.
- Use external `5 V` servo supply.
- Confirm common ground.
- Keep servo horn removed for first powered test.

Physical reason:

```text
unknown neutral + installed horn + powered servo = possible hard-stop impact
```

### 3. Neutral And Limited Sweep

- Install horn after neutral is confirmed.
- Manually verify clearance.
- Switch to `sweep_pitch` or `sweep_yaw`.
- Watch for binding, jitter, or power sag.

The command is limited to `+/-10 deg`, which preserves margin before the `+/-15 deg` mechanical stop.

### 4. IMU Detection

- Connect BNO085 over I2C.
- Confirm `imu_present = 1`.
- Confirm quaternion fields update after the actual driver is added.

### 5. Open-Loop Data Collection

Run:

```text
sweep_pitch
sweep_yaw
step_pitch
step_yaw
```

Save serial CSV logs in:

```text
data/
```

### 6. Analysis Before PID

Use the logs to estimate:

- rise time
- overshoot
- settling time
- steady-state error
- repeatability
- hysteresis/deadband

Only after this should `closed_loop_pid` be added.

## Safety Rules

- Never power servos from Pico USB.
- Never command sweep before verifying neutral.
- Never run with loose wires near the gimbal axes.
- Keep hands clear when servo power is connected.
- Use mechanical stops outside firmware limits.

## Portfolio Interpretation

This bring-up plan demonstrates that the firmware is tied to physical reasoning. The goal is not just "make the servo move." The goal is to measure how the commanded input maps through a real actuator and flexible mechanism into motion, then use that evidence to justify controller design.
