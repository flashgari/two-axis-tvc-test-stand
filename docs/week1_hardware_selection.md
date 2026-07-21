# Week 1 Hardware Selection

## Prototype 1 Decision

Prototype 1 will use the low-cost, fast-bring-up architecture:

| Subsystem | Selected baseline | Reason |
| --- | --- | --- |
| Microcontroller | Raspberry Pi Pico-class RP2040 board | Low cost, deterministic enough for servo/IMU control, strong documentation |
| IMU | BNO085-class fused IMU breakout | Fast attitude bring-up; useful for early closed-loop tests |
| Actuators | Two metal-gear PWM servos | Simple control interface, easy mechanical integration, inexpensive |
| Power | External regulated `5-6 V` servo supply | Prevents servo current spikes from browning out the microcontroller |
| Structure | 3D printed PLA+/PETG gimbal | Fast iteration and easy redesign after first tests |
| Control approach | PID first | Establishes measured hardware performance before model-based control |

## Why Option A

The first prototype needs to generate real hardware data quickly. A more advanced board/sensor/actuator stack can be justified later, but the first engineering win is a working physical mechanism with measured response.

Option A is also cheaper. The Raspberry Pi Pico-class board is roughly an order of magnitude cheaper than a Teensy-class board, while still providing enough PWM, I2C, timing, and serial telemetry for the first test stand.

The lower-cost architecture does not remove the aerospace content of the project. It changes the first research question. Instead of asking whether an expensive actuator can be made to work, Prototype 1 asks whether a real two-axis plant can be characterized well enough to close the loop despite actuator nonidealities. That is a controls-relevant hardware problem: the controller must operate with finite servo bandwidth, backlash, sensor latency, structural compliance, and command saturation.

For a TVC stand, those effects are not side details. They determine the mapping from commanded nozzle deflection to measured attitude response. The same control law that looks stable in simulation can become sluggish, biased, or oscillatory if the actuator has deadband, if the IMU is mounted on a vibrating printed carrier, or if cable loads create an unmodeled restoring/disturbance moment. Prototype 1 is selected specifically because these physical effects can be measured, plotted, and used to justify later design changes.

## Estimated Prototype 1 Cost

Prices vary by vendor and availability. This estimate is for planning only.

| Item | Qty | Planning cost |
| --- | ---: | ---: |
| Raspberry Pi Pico-class board | 1 | `$4-8` |
| BNO085-class IMU breakout | 1 | `$25` |
| Metal-gear servos | 2 | `$20-40` total |
| Servo power supply/regulator | 1 | `$10-20` |
| Breadboard/wires/connectors | 1 set | `$10-20` |
| Bearings/shafts/fasteners | 1 set | `$10-25` |
| 3D print material | 1 set | `$5-15` |
| **Expected total** |  | **about `$85-150`** |

## Hardware Baseline

### Microcontroller

The RP2040/Pico baseline is sufficient for:

- two PWM servo outputs
- I2C IMU communication
- `50-100 Hz` control loop
- USB serial telemetry
- command profile generation

The main limitation is that it is not as powerful as a Teensy 4.1. That is acceptable for Prototype 1 because the controller will start as PID and the test stand is not flight hardware.

The expected loop rate of `50-100 Hz` is adequate for hobby-servo dynamics because the actuator mechanical bandwidth is likely lower than the processor limit. In other words, the first bottleneck is expected to be the electromechanical plant, not floating-point throughput. That makes the Pico a rational first-build choice.

### IMU

The BNO085 baseline provides fused attitude output, which reduces bring-up time. The project should still log raw gyro/accel channels if available, because the engineering story should not be "trust the black box." The BNO085 is used to accelerate the first hardware demonstration, not to avoid sensor reasoning.

This is a deliberate sensor-fusion trade. A fused IMU output reduces the initial burden of writing a full attitude estimator, but it introduces estimator latency, internal filtering, and algorithm behavior that must be acknowledged. The test data should therefore compare command, measured attitude, and measured angular rate so the writeup can separate plant dynamics from sensor/filter dynamics.

### Actuators

Prototype 1 uses hobby-class metal-gear PWM servos. Their known weaknesses are part of the test objective:

- backlash
- deadband
- finite bandwidth
- gear compliance
- current spikes
- no true torque telemetry

The project should measure these limitations instead of pretending they do not exist.

Servo limitations are especially relevant for thrust vector control because actuator lag creates phase delay in the feedback loop. Too much delay reduces phase margin and can turn an otherwise stable controller into an oscillatory one. Backlash and deadband also create a region where small control efforts do not immediately produce nozzle motion, which is exactly the kind of nonlinearity that should appear in step-response and small-command tracking tests.

### Structure

The first gimbal should be 3D printed and deliberately easy to modify. The design should include:

- outer frame
- inner gimbal/nozzle carrier
- actuator mounts
- mechanical hard stops
- IMU mount
- wire strain relief
- accessible fasteners

## Prototype 1 Acceptance Criteria

Prototype 1 is successful when it can:

1. Move both axes through at least `+/-10 deg`.
2. Read and log IMU attitude/rate.
3. Record open-loop step response.
4. Track a small single-axis command in closed loop.
5. Produce commanded-vs-measured plots.
6. Document at least one physical limitation and design iteration.

## Week 1 Deliverables

- [x] Hardware baseline selected
- [x] Cost estimate
- [x] Actuator sizing first pass
- [x] CAD concept definition
- [x] Wiring plan
- [x] Purchase checklist
- [ ] Final vendor links before purchase
- [ ] First CAD model
