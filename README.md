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
- [ ] Final component selection
- [ ] CAD first-pass layout
- [ ] Firmware bring-up plan

## Near-Term Build Plan

1. Finalize actuator, IMU, and microcontroller selection.
2. Design first-pass gimbal CAD with mechanical stops.
3. Build firmware skeleton for actuator commands and serial telemetry.
4. Calibrate IMU and actuator neutral positions.
5. Run open-loop step-response tests.
6. Implement closed-loop PID tracking.
7. Document failures, backlash, flex, saturation, noise, and design iterations.

## Safety Scope

This project starts with a mock engine/nozzle only. No live motors, pyrotechnics, high-pressure systems, or combustion hardware are part of the initial test stand.

The test article is a controls and mechanisms platform, not a propulsion test.
