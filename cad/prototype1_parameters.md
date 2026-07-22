# Prototype 1 CAD Parameters

Current baseline date: `2026-07-21`

This file records the dimensional assumptions used for the first CAD layout. Vendor values are used to start the model, but all critical dimensions must be measured with calipers after parts arrive.

## Coordinate Frames

The CAD model uses a right-handed bench frame:

```text
+x = pitch-axis reference direction
+y = yaw-axis reference direction
+z = vertical/up
```

The gimbal is treated as a nested two-axis mechanism:

```text
fixed base -> yaw frame -> pitch/nozzle carrier -> mock nozzle and IMU
```

## Servo Baseline

Selected actuator: Hitec HS-625MG standard metal-gear PWM servo.

| Parameter | CAD baseline | Source / note |
| --- | ---: | --- |
| Body length | `40.6 mm` | Hitec published dimension |
| Body width | `19.8 mm` | Hitec published dimension |
| Body height | `37.8 mm` | Hitec published dimension |
| Mass | `55.2 g` | Hitec published weight |
| Spline | `24T`, about `6 mm` class | Hitec/ServoCity published spline family |
| Wire length | `300 mm` | ServoCity published value |
| Stall torque at `6.0 V` | `6.8 kg-cm` | Hitec/ServoCity published value |
| No-load speed at `6.0 V` | `0.15 s/60 deg` | Hitec/ServoCity published value |
| Deadband | `8 us` | ServoCity published value |

## Rev A Mounting Assumptions

The OpenSCAD baseline includes slotted servo mounting holes rather than fixed exact holes. This is intentional: standard-size servo mounting patterns vary slightly, and printed parts will have tolerance error.

| Parameter | Rev A placeholder | Note |
| --- | ---: | --- |
| mount slot length | `9.0 mm` | Allows alignment adjustment after printing. |
| mount slot width | `3.4 mm` | Intended for M3-class clearance; verify screw choice. |
| nominal long-axis hole span | `49.5 mm` | Standard-servo placeholder; verify on HS-625MG body. |
| nominal cross-axis hole span | `27.5 mm` | Standard-servo placeholder; verify on HS-625MG body. |
| supported shaft diameter | `4.0 mm` | Placeholder for small shaft/bushing concept. |
| bearing/bushing envelope | `8.0 mm` | Placeholder until hardware choice is finalized. |

The slotted mount design reduces alignment-induced friction. If the servo is forced into a misaligned printed mount, the output shaft can see side load, which increases hysteresis and makes step-response data harder to interpret.

## First Layout Assumptions

| Quantity | Value | Reason |
| --- | ---: | --- |
| Firmware command limit | `+/-10 deg` | Keeps motion away from hard stops during tests. |
| Mechanical hard stop | about `+/-15 deg` | Protects servo/linkage from overtravel. |
| Base plate | `160 x 120 x 6 mm` | Large enough for two standard servos and clamps. |
| Outer yaw frame width | `95 mm` | Leaves clearance around inner pitch carrier. |
| Outer yaw frame height | `95 mm` | Gives visual and wiring clearance. |
| Inner pitch carrier width | `55 mm` | Holds mock nozzle and IMU platform. |
| Mock nozzle length | `85 mm` | Large enough to see motion in video. |
| Mock nozzle diameter | `24 mm` | Lightweight printable surrogate. |
| IMU pad | `28 x 22 mm` | Fits common BNO085 breakout footprint envelope. |
| Minimum moving-wire slack | `40 mm` | Reduces cable-induced restoring moment. |

## Rev A Mass-Property Estimates

Detailed assumptions are documented in [rev_a_mass_inertia_estimate.md](rev_a_mass_inertia_estimate.md).

| Axis | Moving mass estimate | Inertia estimate | Gravity moment estimate |
| --- | ---: | ---: | ---: |
| pitch | `73 g` | `3.0e-5 kg m^2` | `0.018 N m` |
| yaw | `200 g` | `3.0e-4 kg m^2` | `0.039 N m` |

These estimates suggest the prototype is not static-torque limited. The more important Rev A risk is dynamic behavior: servo speed, deadband, gear backlash, frame compliance, and cable-induced bias.

## Physics Inputs For CAD

The CAD layout must support the actuator sizing model:

```text
tau_gravity = m g r
I_axis theta_ddot + c theta_dot + k theta ~= tau_servo + tau_disturbance
```

Key design implications:

- Keep the moving center of mass close to both rotation axes to reduce gravity bias.
- Avoid routing wires so they behave like torsion springs.
- Keep the IMU on the moving nozzle carrier, not the fixed base.
- Keep hard stops independent of the servo internal mechanical limits.
- Make the servo mounts adjustable enough to correct alignment after printing.

## Dimensions To Verify After Parts Arrive

- servo body length, width, height
- output spline diameter and horn thickness
- horn screw diameter and thread
- servo mounting-ear hole spacing
- servo wire exit location
- BNO085 board size and hole pattern
- actual printed nozzle/carrier mass and center of mass

The first CAD revision should be updated after these measurements before any final print is treated as a test article.
