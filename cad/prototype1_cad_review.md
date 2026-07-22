# Prototype 1 CAD Review Notes

## Design Intent

Prototype 1 is a benchtop two-axis TVC mechanism for controls testing. It is not a flight-weight thrust-vector mount. The CAD should make the plant easy to instrument, inspect, modify, and explain.

Primary objectives:

1. Hold a mock nozzle on two controlled axes.
2. Keep the moving center of mass close to the gimbal axes.
3. Provide hard stops outside the firmware command range.
4. Mount the IMU on the controlled moving body.
5. Route wires so they do not dominate the measured restoring torque.
6. Keep the assembly printable and repairable.

## Baseline CAD Files

| File | Purpose |
| --- | --- |
| `prototype1_parameters.md` | Dimensional assumptions and physical rationale. |
| `prototype1_gimbal_baseline.scad` | Parametric first-pass concept model. |
| `exports/prototype1_cad_baseline.svg` | Static layout preview for README/review. |

## Mechanical Architecture

The first concept uses:

- fixed base plate
- yaw servo mounted to the base
- outer yaw frame
- pitch servo mounted near the outer frame
- inner pitch/nozzle carrier
- mock nozzle
- IMU pad on the moving carrier
- visual references for `+/-15 deg` hard stops

The model intentionally separates the firmware command limit from the mechanical limit:

```text
firmware limit: +/-10 deg
mechanical stop: about +/-15 deg
```

This gives enough room for calibration error without allowing the servo or linkage to hit its internal mechanical limit during normal tests.

## Upper-Division Physical Rationale

A TVC test stand is a coupled electromechanical plant, not just a rotating bracket. In small-angle form, each axis can be interpreted as:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The CAD directly affects every term:

| Term | CAD driver | Design implication |
| --- | --- | --- |
| `I_axis` | moving nozzle/carrier/servo mass distribution | keep mass near the rotation axes where practical |
| `c` | bearing friction, servo internal damping, rubbing surfaces | avoid printed-on-printed rubbing as the primary bearing if it causes hysteresis |
| `k` | printed-frame flex, cable stiffness, gravity coupling | strain-relieve wires and keep the CM close to the axes |
| `tau_servo` | horn geometry, spline alignment, servo voltage | use traceable servo specs and avoid binding |
| `tau_disturbance` | cable preload, misalignment, bench vibration | make disturbances visible and repeatable during tests |

The CAD baseline should therefore be evaluated by how well it supports clean system identification. The first open-loop step tests should reveal whether the dominant error source is actuator lag, backlash, structural flex, sensor filtering, or wire-induced bias.

## Design Review Checklist

Before printing Rev A:

- [ ] Confirm HS-625MG body dimensions with calipers.
- [ ] Confirm mounting-ear hole spacing.
- [ ] Confirm horn thickness, spline fit, and screw size.
- [ ] Confirm BNO085 board hole spacing and connector clearance.
- [ ] Estimate moving mass and center of mass from CAD.
- [ ] Check `+/-10 deg` motion clearance without wire strain.
- [ ] Check hard stops engage before servo/linkage binding.
- [ ] Confirm the base can be clamped or weighted during tests.
- [ ] Add labels/arrows for pitch, yaw, and IMU axes.

## Rev A Manufacturing Notes

- Use PLA+ for speed if PETG is unavailable; use PETG if extra toughness is needed.
- Print servo mounts with enough wall thickness around screw holes.
- Prefer heat-set inserts for parts expected to be removed repeatedly.
- Use fillets around frame corners to reduce stress concentration and print cracking.
- Avoid support-heavy geometry in the first revision.
- Keep fasteners accessible without disassembling the full gimbal.

## Expected First-Revision Failure Modes

These are acceptable if they are measured and used to iterate:

- servo backlash produces different measured neutral positions depending on approach direction
- printed frame flex causes slow settling or overshoot
- wire drag creates a steady-state bias torque
- IMU vibration corrupts rate measurements during fast servo steps
- servo power sag causes intermittent jitter or telemetry resets

The first CAD is successful if it produces a testable mechanism and exposes these effects clearly enough to improve Rev B.
