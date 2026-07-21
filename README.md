# Two-Axis Thrust Vector Control Test Stand

Hardware GNC portfolio project to design, build, and test a benchtop two-axis thrust-vector-control mechanism from scratch.

## Project Goal

Build a physical two-axis gimbal test stand that points a mock rocket engine/nozzle, measures actuator and attitude response, runs closed-loop control on embedded hardware, and produces real test data.

This project is intentionally hardware-first. The objective is to demonstrate the full engineering loop:

```text
requirements -> CAD -> fabrication -> electronics -> firmware -> calibration -> test data -> iteration
```

## Why This Project

The previous 6-DOF rocket simulator demonstrated nonlinear flight dynamics, TVC allocation, LQR control, actuator dynamics, and robustness verification in software. This project turns that GNC stack into a physical test article.

The portfolio claim this project is designed to support:

> Personally designed, built, tested, and iterated a two-axis TVC hardware test stand with embedded sensing, actuation, closed-loop control, and measured performance data.

## Target Capabilities

| Capability | Target |
| --- | --- |
| Gimbal axes | 2-axis pitch/yaw |
| Angular range | At least `+/-10 deg` mechanical travel |
| Command tracking | Less than `1 deg` steady-state error after calibration |
| Step response | Settling time under `0.5 s` for small commands |
| Sensing | IMU attitude/rate measurement plus actuator command telemetry |
| Control | PID first, then optional model-based/LQR-inspired controller |
| Data logging | CSV logs for command, measured angle, IMU rate, error, and actuator output |
| Demonstration | Video of open-loop step response, closed-loop tracking, and disturbance rejection |

## Prototype 1 Hardware Baseline

Prototype 1 uses the lowest-cost architecture that still supports a real controls experiment. The intent is not to imitate a flight-qualified TVC actuator on the first pass. The intent is to build a benchtop plant with measurable inertia, friction, backlash, actuator saturation, sensor noise, and closed-loop tracking behavior.

| Subsystem | Selection |
| --- | --- |
| Microcontroller | Raspberry Pi Pico-class RP2040 board |
| IMU | BNO085-class fused IMU breakout |
| Actuators | Two metal-gear PWM servos |
| Power | External regulated `5-6 V` servo supply |
| Structure | 3D printed PLA+/PETG gimbal |
| Control | PID first, model-based comparison later |

Estimated Prototype 1 budget: about `$85-150` before tools.

This baseline was selected because it gets to hardware test data quickly: the Pico is sufficient for a `50-100 Hz` embedded control loop, the BNO085 shortens attitude bring-up while still allowing sensor-performance discussion, metal-gear servos expose real actuator nonidealities, and a printed structure allows rapid iteration after the first measured step-response and disturbance-rejection tests.

## Week 1 Engineering Basis

The first sizing pass treats the gimbal/nozzle carrier as a rigid body with an offset center of mass. If the moving assembly has mass `m` and its center of mass is offset by `r` from the rotation axis, the static gravity moment is

```text
tau_gravity = m g r
```

Using `m = 0.20 kg` and `r = 0.04 m` gives `tau_gravity = 0.078 N m`, or about `0.80 kg-cm`. With a `3x` static margin, the first servo target is at least `2.4 kg-cm`, so Prototype 1 specifies `>= 5 kg-cm` metal-gear servos to leave margin for friction, cable drag, printed-frame compliance, and transient acceleration torque.

The more important controls question is not only whether the servo can hold the load. A TVC mechanism must track commanded angular deflection with finite bandwidth, limited authority, mechanical deadband, and imperfect sensing. That is why the first hardware tests will measure commanded angle, IMU-measured attitude/rate, settling time, overshoot, repeatability, and any neutral bias caused by wire loads or gimbal friction.

## System Architecture

```text
host computer
  -> sends test profile / receives serial logs

microcontroller
  -> reads IMU
  -> commands two actuators
  -> runs control loop
  -> streams telemetry

mechanical test stand
  -> fixed base
  -> two-axis gimbal
  -> mock engine/nozzle
  -> mechanical stops
```

## Repository Layout

```text
cad/        CAD notes, exported drawings, manufacturing notes
data/       raw test logs
docs/       requirements, safety, architecture, test plans, BOM trade studies
firmware/   embedded controller source and calibration sketches
media/      photos and demo video links
plots/      generated test plots
tests/      analysis scripts and hardware-in-the-loop test notes
```

## Week 0 Deliverables

- [x] Requirements document
- [x] System architecture
- [x] Safety plan
- [x] Preliminary hardware trade study
- [x] Test plan
- [x] Prototype 1 component architecture selected
- [x] Actuator sizing first pass
- [x] Wiring plan
- [x] CAD concept definition
- [ ] Final vendor links before purchase
- [ ] First CAD model
- [ ] Firmware bring-up plan

## Near-Term Build Plan

1. Confirm final vendor links and physical dimensions.
2. Design first-pass gimbal CAD with mechanical stops.
3. Build firmware skeleton for actuator commands and serial telemetry.
4. Calibrate IMU and actuator neutral positions.
5. Run open-loop step-response tests.
6. Implement closed-loop PID tracking.
7. Document failures, backlash, flex, saturation, noise, and design iterations.

## Safety Scope

This project starts with a mock engine/nozzle only. No live motors, pyrotechnics, high-pressure systems, or combustion hardware are part of the initial test stand.

The test article is a controls and mechanisms platform, not a propulsion test.
