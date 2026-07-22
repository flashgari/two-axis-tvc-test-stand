# Hardware Calibration And First-Test Worksheet

## Objective

Create a disciplined bench-test procedure for the first powered Rev A hardware tests. The goal is to separate actuator, sensor, structure, and assembly effects before attempting closed-loop control.

The first hardware campaign answers one technical question:

```text
Does the measured gimbal response match the pre-hardware dynamic model closely enough
to justify the Rev A plant assumptions?
```

The relevant plant model is:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
delta_dot = (delta_cmd - delta) / tau_servo_lag
tau_servo = clamp(K_servo (delta - theta), -tau_limit, +tau_limit)
```

This worksheet exists so the first test data can be interpreted physically instead of being treated as a simple motion demo.

## Pre-Test Configuration Record

Complete this table before powering the servos with the mechanism assembled.

| Item | Value / notes |
| --- | --- |
| Test date |  |
| Operator |  |
| Printed material |  |
| Layer height / infill / wall count |  |
| Pitch servo serial/label |  |
| Yaw servo serial/label |  |
| Servo supply voltage, no load |  |
| Servo supply voltage, moving |  |
| Pico USB power source |  |
| IMU mount location |  |
| IMU axis convention confirmed | yes / no |
| Horns removed for first neutral test | yes / no |
| Mechanical hard stops installed | yes / no |
| Wiring strain relief installed | yes / no |
| Emergency power disconnect available | yes / no |

## Servo Neutral Calibration

Run servo-neutral calibration with the servo horns removed first. This avoids driving the printed mechanism into a hard stop if the PWM neutral assumption is wrong.

| Axis | Command PWM | Observed servo behavior | Accepted neutral PWM | Notes |
| --- | ---: | --- | ---: | --- |
| pitch | `1500 us` |  |  |  |
| yaw | `1500 us` |  |  |  |

After horns are installed, record the mechanical zero:

| Axis | Neutral PWM | Mechanical angle at neutral | Horn spline adjustment needed | Final zero offset |
| --- | ---: | ---: | --- | ---: |
| pitch |  |  |  |  |
| yaw |  |  |  |  |

Upper-division interpretation:

- A neutral angle offset is not just an assembly inconvenience. In the plant equation it behaves like either an actuator bias or a constant disturbance torque, depending on whether the error comes from spline indexing, center-of-mass offset, wire preload, or gravity coupling.
- If the nozzle rests off-zero while the commanded PWM is neutral, the controller will spend steady-state authority canceling a DC moment before it can reject dynamic disturbances.
- If the neutral point changes after moving positive versus negative, the mechanism has backlash or Coulomb-friction hysteresis. That violates the simple linear prediction model and must be documented before tuning gains.

## IMU Calibration And Axis Check

The BNO085 fused attitude estimate is useful only if the sensor axes are mapped correctly to the gimbal axes.

| Check | Expected result | Pass/fail | Notes |
| --- | --- | --- | --- |
| IMU detected over I2C | telemetry reports valid sensor status |  |  |
| Static zero repeatability | measured pitch/yaw remain near zero after reset |  |  |
| Positive pitch hand deflection | measured pitch sign matches convention |  |  |
| Positive yaw hand deflection | measured yaw sign matches convention |  |  |
| Rate sign check | gyro sign matches angle derivative |  |  |

Physical interpretation:

- A sign error creates positive feedback in closed-loop testing, which can drive the actuator into a stop even if the controller code is mathematically correct.
- Static attitude drift enters the measured output as a low-frequency bias. In a PID loop, integral action can mistake that sensor bias for real pointing error and command a false trim torque.
- Excessive vibration or loose IMU mounting appears as high-frequency measured rate content. That contaminates derivative feedback and can make a mechanically stable gimbal look unstable in telemetry.

## First Open-Loop Step Tests

Use small-amplitude open-loop commands first. Recommended order:

| Test ID | Axis | Command | Repeats | Purpose |
| --- | --- | --- | ---: | --- |
| `PITCH_STEP_2DEG_A` | pitch | `0 -> +2 deg -> 0` | 3 | low-risk pitch bandwidth check |
| `PITCH_STEP_5DEG_A` | pitch | `0 -> +5 deg -> 0` | 3 | compare with pre-hardware prediction |
| `YAW_STEP_2DEG_A` | yaw | `0 -> +2 deg -> 0` | 3 | low-risk yaw bandwidth check |
| `YAW_STEP_5DEG_A` | yaw | `0 -> +5 deg -> 0` | 3 | compare with pre-hardware prediction |
| `PITCH_HYST_5DEG_A` | pitch | `-5 -> +5 -> -5 deg` | 3 | backlash/friction check |
| `YAW_HYST_5DEG_A` | yaw | `-5 -> +5 -> -5 deg` | 3 | backlash/friction check |

CSV logs should use the template columns in [data/templates/hardware_step_log_template.csv](../data/templates/hardware_step_log_template.csv).

## First-Test Pass / Investigate Criteria

These are not final product requirements. They are first-build screening criteria.

| Metric | Investigate if | Physical implication |
| --- | --- | --- |
| response delay | above `0.10 s` | servo lag, command transport delay, IMU filtering, or power issue |
| rise time | more than `2x` pre-hardware prediction | higher inertia, lower servo torque, binding, or voltage sag |
| overshoot | above `20%` on small steps | low damping, compliant frame, loose horn, aggressive internal servo loop |
| settling time | above `1.0 s` | insufficient damping, geartrain slop, frame flex, or sensor filtering |
| steady-state error | above `1.0 deg` | CM bias, wire preload, horn offset, deadband, or calibration error |
| hysteresis bias | above `0.5 deg` | backlash, spline slop, bearing friction, or asymmetric cable routing |

## Comparing Hardware To Prediction

After each measured run:

```bash
python3 scripts/analyze_step_response.py data/<log>.csv --axis pitch
python3 scripts/plot_step_response.py data/<log>.csv --axis pitch
```

Then compare the measured metrics against:

- `data/examples/prehardware_pitch_step_prediction.pitch.metrics.json`
- `data/examples/prehardware_yaw_step_prediction.yaw.metrics.json`

Interpretation guide:

- Slower measured rise time means the effective angular acceleration `theta_ddot = tau_net / I_axis` is lower than predicted. That can happen because the real inertia is higher, useful servo torque is lower, friction consumes torque, or the servo supply voltage collapses under load.
- Larger measured steady-state error means the equilibrium torque balance is wrong. The real system likely has a larger constant disturbance torque, a larger elastic preload, or a servo deadband region where commanded PWM changes do not produce proportional output torque.
- More overshoot means the damping ratio is lower than predicted. In a printed mechanism, this can come from flexible side frames, compliance in the servo horn, bearing clearance, or an internal servo loop that injects phase lag near the structural mode.
- Yaw should generally be slower than pitch because the yaw servo rotates the outer frame plus the entire pitch subsystem. For the same torque limit, increasing `I_axis` reduces angular acceleration and usually increases settling time.
- If repeated tests disagree with each other, the limiting issue is probably not the linear plant. It is more likely backlash, Coulomb friction, loose fasteners, cable motion, IMU mounting, or supply noise.

## Required Photo / Video Evidence

For portfolio credibility, record:

- a still photo of the unpowered assembled test stand
- a still photo showing wiring strain relief and servo power routing
- a short video of servo-neutral testing with horns removed
- a short video of a `+/-5 deg` pitch step
- a short video of a `+/-5 deg` yaw step
- a screenshot of the corresponding plotted telemetry

The final writeup should pair each video with the measured CSV and explain the physics behind the motion.
