# Preliminary BOM Trade Study

This is a Week 0 trade study, not a final purchase list. Exact component availability, current pricing, and datasheets should be verified before buying parts.

## Selection Philosophy

The first build should prioritize:

- fast assembly
- easy debugging
- robust data logging
- enough actuator torque for a mock nozzle
- clean wiring
- low risk

It should not optimize for minimum mass or flight packaging. This is a benchtop test article.

## Candidate Subsystems

### Microcontroller

| Option | Strength | Risk |
| --- | --- | --- |
| Teensy-class board | Fast control loop, good serial logging, many PWM options | Higher cost |
| ESP32-class board | Inexpensive, capable, wireless optional | Timing/library complexity |
| Raspberry Pi Pico-class board | Inexpensive, deterministic enough, good documentation | More manual library integration |
| Arduino-class board | Easy bring-up | May be limiting for logging/control bandwidth |

Recommended direction for first build: choose a board with reliable PWM, I2C/SPI, and high-rate serial logging.

### IMU

| Option | Strength | Risk |
| --- | --- | --- |
| BNO085-class fused IMU | Convenient attitude output | Fusion behavior can hide raw dynamics |
| ICM-20948-class IMU | Raw gyro/accel/mag access | More calibration/filtering work |
| MPU-6050-class IMU | Cheap and common | Older sensor, noisier, fewer features |

Recommended direction: start with a convenient fused IMU for bring-up, but log raw gyro/accel if available so the project still demonstrates sensor reasoning.

### Actuators

| Option | Strength | Risk |
| --- | --- | --- |
| Metal-gear hobby servos | Simple PWM, easy mechanical integration | Backlash, limited telemetry |
| Digital bus servos | Better control/feedback options | More protocol complexity |
| BLDC gimbal motors | Smooth motion and control depth | Much harder electronics/control project |

Recommended direction: use metal-gear servos for prototype 1, then document backlash and bandwidth limits honestly.

### Mechanical Structure

| Option | Strength | Risk |
| --- | --- | --- |
| 3D-printed PLA/PETG | Fast iteration | Flex, creep, heat sensitivity |
| Laser-cut plates | Flat and stiff | Less geometry freedom |
| Aluminum brackets | Stiffer and more professional | Slower fabrication |

Recommended direction: 3D print the first gimbal so failures can be corrected quickly.

## First-Build Hardware Targets

| Item | Target spec |
| --- | --- |
| Actuator range | At least `+/-10 deg` achieved gimbal motion |
| Actuator torque | Enough to move mock nozzle with margin |
| IMU update rate | At least `50 Hz`, preferably `100 Hz+` |
| Logging | CSV over USB serial |
| Power | Separate regulated actuator supply |
| Structure | Rigid base, accessible fasteners, mechanical stops |

## Final BOM Fields To Fill Before Purchase

| Item | Selected part | Quantity | Reason | Source | Cost |
| --- | --- | ---: | --- | --- | ---: |
| Microcontroller | TBD | 1 | TBD | TBD | TBD |
| IMU | TBD | 1 | TBD | TBD | TBD |
| Pitch actuator | TBD | 1 | TBD | TBD | TBD |
| Yaw actuator | TBD | 1 | TBD | TBD | TBD |
| Power supply/regulator | TBD | 1 | TBD | TBD | TBD |
| Bearings/shafts/fasteners | TBD | TBD | TBD | TBD | TBD |
| Printed material | TBD | TBD | TBD | TBD | TBD |

## Trade Study Takeaway

The first prototype should be simple enough to build quickly but instrumented well enough to generate real engineering plots. The goal is not a perfect TVC mechanism on revision 1; the goal is a measured design-build-test loop with clear iteration.
