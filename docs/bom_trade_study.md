# Preliminary BOM Trade Study

This began as a Week 0 trade study. Prototype 1 now uses the low-cost Option A baseline: Raspberry Pi Pico-class microcontroller, BNO085-class IMU, metal-gear PWM servos, external servo power, and a 3D printed structure. Exact component availability, current pricing, and datasheets should still be verified before buying parts.

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

Selected Prototype 1 direction: Raspberry Pi Pico-class board. It is low cost and provides enough PWM, I2C, timing, and USB serial telemetry for the first test stand.

### IMU

| Option | Strength | Risk |
| --- | --- | --- |
| BNO085-class fused IMU | Convenient attitude output | Fusion behavior can hide raw dynamics |
| ICM-20948-class IMU | Raw gyro/accel/mag access | More calibration/filtering work |
| MPU-6050-class IMU | Cheap and common | Older sensor, noisier, fewer features |

Selected Prototype 1 direction: BNO085-class fused IMU. It reduces bring-up time and still supports a meaningful sensor/control test if raw gyro/accel channels are logged where available.

### Actuators

| Option | Strength | Risk |
| --- | --- | --- |
| Metal-gear hobby servos | Simple PWM, easy mechanical integration | Backlash, limited telemetry |
| Digital bus servos | Better control/feedback options | More protocol complexity |
| BLDC gimbal motors | Smooth motion and control depth | Much harder electronics/control project |

Selected Prototype 1 direction: metal-gear PWM servos. Their backlash, deadband, and finite bandwidth are not hidden; they become part of the measured hardware characterization.

### Mechanical Structure

| Option | Strength | Risk |
| --- | --- | --- |
| 3D-printed PLA/PETG | Fast iteration | Flex, creep, heat sensitivity |
| Laser-cut plates | Flat and stiff | Less geometry freedom |
| Aluminum brackets | Stiffer and more professional | Slower fabrication |

Selected Prototype 1 direction: 3D print the first gimbal so failures can be corrected quickly.

## First-Build Hardware Targets

| Item | Target spec |
| --- | --- |
| Actuator range | At least `+/-10 deg` achieved gimbal motion |
| Actuator torque | Enough to move mock nozzle with margin |
| IMU update rate | At least `50 Hz`, preferably `100 Hz+` |
| Logging | CSV over USB serial |
| Power | Separate regulated actuator supply |
| Structure | Rigid base, accessible fasteners, mechanical stops |

## Prototype 1 BOM Baseline

| Item | Selected part | Quantity | Reason | Source | Cost |
| --- | --- | ---: | --- | --- | ---: |
| Microcontroller | Raspberry Pi Pico-class RP2040 board | 1 | low cost, adequate timing/PWM/I2C | TBD | `$4-8` |
| IMU | BNO085-class breakout | 1 | fast attitude bring-up | TBD | about `$25` |
| Pitch actuator | metal-gear PWM servo | 1 | simple first prototype actuation | TBD | TBD |
| Yaw actuator | metal-gear PWM servo | 1 | simple first prototype actuation | TBD | TBD |
| Power supply/regulator | external `5-6 V` servo supply | 1 | avoids USB/microcontroller brownout | TBD | TBD |
| Bearings/shafts/fasteners | TBD | TBD | TBD | TBD | TBD |
| Printed material | PLA+/PETG | TBD | fast iteration | local/available | TBD |

## Trade Study Takeaway

The first prototype should be simple enough to build quickly but instrumented well enough to generate real engineering plots. The goal is not a perfect TVC mechanism on revision 1; the goal is a measured design-build-test loop with clear iteration.
