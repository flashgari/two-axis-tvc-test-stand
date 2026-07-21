# Test Plan

## Test Philosophy

The project should prove performance with data, not just video. Every major claim should map to a repeatable test and a plot.

## Test 1: Mechanical Range Test

Purpose: verify physical travel and stops.

Procedure:

1. Power off the system.
2. Move gimbal manually through pitch and yaw.
3. Confirm hard stops prevent overtravel.
4. Record measured range.

Pass criteria:

- Both axes move at least `+/-10 deg`.
- No binding through the expected range.
- Wires do not restrict motion.

## Test 2: Actuator Neutral Calibration

Purpose: map PWM command to approximate gimbal angle.

Procedure:

1. Command neutral PWM.
2. Measure physical neutral.
3. Sweep small increments around neutral.
4. Record command vs measured angle.

Plot:

```text
actuator_command_us vs measured_angle_deg
```

Pass criteria:

- Repeatable neutral position.
- Monotonic command-to-angle response.

## Test 3: Open-Loop Step Response

Purpose: characterize actuator dynamics before closing the loop.

Procedure:

1. Command a small pitch step.
2. Log measured angle and gyro rate.
3. Repeat for yaw.
4. Repeat for larger but safe commands.

Metrics:

- rise time
- settling time
- overshoot
- steady-state error
- backlash/deadband estimate

## Test 4: Closed-Loop Single-Axis PID

Purpose: demonstrate controlled tracking on one axis.

Procedure:

1. Enable pitch-axis PID only.
2. Command small step input.
3. Tune gains conservatively.
4. Repeat for yaw axis.

Plot:

```text
commanded_angle_deg, measured_angle_deg, tracking_error_deg, actuator_output
```

Pass criteria:

- Settling time under `0.5 s` for small commands.
- Steady-state error under `1 deg`.
- No sustained oscillation.

## Test 5: Two-Axis Tracking

Purpose: demonstrate coupled operation.

Procedure:

1. Command pitch and yaw steps separately.
2. Command combined pitch/yaw profile.
3. Log cross-axis coupling.

Physical interpretation:

If a pitch command produces yaw motion, the mechanism has cross-axis coupling from geometry, flex, linkage alignment, sensor placement, or controller coupling.

## Test 6: Disturbance Rejection

Purpose: show closed-loop recovery from a small external perturbation.

Procedure:

1. Hold neutral command.
2. Apply a small manual disturbance to the mock nozzle.
3. Release.
4. Log response.

Pass criteria:

- Gimbal returns near neutral.
- Response is damped.
- No actuator saturation or mechanical binding.

## Test Report Template

Each test should produce:

- date
- hardware revision
- firmware commit
- test objective
- setup photo
- raw CSV log
- plot
- metrics
- observations
- failure/iteration notes

## Minimum Portfolio Plot Set

- open-loop actuator step response
- closed-loop command tracking
- tracking error vs time
- disturbance rejection response
- command vs measured calibration curve
