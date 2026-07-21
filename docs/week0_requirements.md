# Week 0 Requirements

## Mission Statement

Design, build, and test a benchtop two-axis thrust-vector-control test stand that demonstrates embedded control, actuator characterization, sensor integration, and measured closed-loop performance.

## Primary Requirement

The system shall command and measure two-axis gimbal motion for a mock rocket nozzle and demonstrate closed-loop tracking and disturbance rejection using real hardware data.

## Functional Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| FR-1 | The mechanism shall provide two rotational degrees of freedom representing pitch and yaw TVC. | CAD inspection and manual range test |
| FR-2 | The gimbal shall provide at least `+/-10 deg` mechanical travel on both axes. | Protractor/IMU measurement |
| FR-3 | The firmware shall command both actuators independently. | Serial command test |
| FR-4 | The firmware shall log time, command angle, measured angle, angular rate, tracking error, and actuator output. | CSV log inspection |
| FR-5 | The system shall run a repeatable step-response test profile. | Test script and plotted response |
| FR-6 | The system shall run closed-loop tracking on at least one axis, then both axes. | Closed-loop test data |
| FR-7 | The system shall include mechanical stops that prevent actuator overtravel. | Physical inspection |
| FR-8 | The system shall use a mock engine/nozzle for initial testing. | Physical inspection |

## Performance Targets

| Metric | Target | Rationale |
| --- | ---: | --- |
| Small-step settling time | `< 0.5 s` | Demonstrates usable actuator bandwidth |
| Steady-state command error | `< 1 deg` | Shows calibration and control accuracy |
| Overshoot | `< 20%` for first controlled tests | Keeps tuning conservative |
| Sample/log rate | `>= 50 Hz` | Captures servo-scale dynamics |
| Mechanical travel | `+/-10 deg` minimum | Representative TVC envelope |

## Engineering Requirements

- CAD shall define the base, inner gimbal, outer gimbal, mock nozzle, actuator mounts, and mechanical stops.
- The first prototype shall be easy to disassemble and modify.
- Wiring shall be strain-relieved so actuator motion does not pull on connectors.
- The test stand shall be stable on a bench without being handheld during tests.
- All tests shall start with low-speed/small-angle commands before larger profiles.

## Portfolio Requirements

The project shall produce:

- CAD screenshots and exported drawings
- Bill of materials and trade study
- Wiring diagram
- Firmware source
- Calibration procedure
- Open-loop step-response plot
- Closed-loop tracking plot
- Disturbance rejection plot
- Demo video
- Design iteration log

## Out Of Scope For Initial Build

- Live rocket motors
- Pyrotechnics
- Combustion testing
- Pressurized propellant systems
- Flight testing
- High-voltage systems

## Success Criteria

The Week 0-to-final project is successful if it demonstrates a physical test stand that:

1. Was designed in CAD.
2. Was fabricated and assembled.
3. Uses real embedded sensors and actuators.
4. Runs repeatable tests.
5. Produces plots from measured data.
6. Documents at least one design issue and iteration.
