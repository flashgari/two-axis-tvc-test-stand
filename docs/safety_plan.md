# Safety Plan

## Safety Scope

This project begins as a benchtop controls/mechanisms test stand. It does not use live rocket motors, propellant, combustion, pyrotechnics, compressed gas, or flight hardware.

## Hard Rules

- No live motors during initial development.
- No pyrotechnics.
- No combustion testing.
- No pressurized propellant systems.
- No tests while holding the mechanism by hand.
- No actuator tests without mechanical stops installed.
- No high-current actuator supply without common ground and basic fuse/current limiting.

## Bench Safety Controls

| Hazard | Control |
| --- | --- |
| Servo pinch points | Keep fingers clear during powered tests; use low-speed commands first |
| Overtravel | Add mechanical stops and firmware angle limits |
| Brownout/reset | Use separate actuator supply and common ground |
| Loose mechanism | Clamp or weight base during tests |
| Wire snag | Strain relief and route wires away from moving axes |
| Hot regulator/servo | Start with short-duration tests and inspect temperatures |

## Test Readiness Checklist

Before every powered test:

- [ ] Mechanism is secured to the bench.
- [ ] Mechanical stops are installed.
- [ ] Actuator range limits are enabled in firmware.
- [ ] Wires cannot enter the gimbal path.
- [ ] Power supply voltage/current are appropriate.
- [ ] Emergency unplug/switch is reachable.
- [ ] Test starts from neutral position.
- [ ] Logging is enabled.

## Test Progression

1. Manual unpowered range test.
2. Low-speed actuator movement without IMU control.
3. Open-loop small-angle step commands.
4. Larger open-loop commands.
5. Single-axis closed-loop tests.
6. Two-axis closed-loop tests.
7. Disturbance rejection by small manual perturbation.

## Safety Statement For Portfolio

The test stand is intentionally scoped as a non-propulsive GNC hardware platform. All initial tests use a mock nozzle to validate sensing, actuation, controls, and data acquisition before any propulsion-related application is considered.
