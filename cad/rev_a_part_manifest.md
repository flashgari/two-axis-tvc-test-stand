# Rev A Printable Part Manifest

This manifest defines the first separated printable parts for Prototype 1. The combined layout STL remains useful for design review, but fabrication should use separated parts so each component can be oriented, inspected, and iterated independently.

## Physical Model Used Throughout

Each axis of the gimbal is interpreted as:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The part split is not just a CAD organization choice. It lets each physical contribution be controlled:

- `I_axis`: reduced by keeping moving parts compact and hollow where possible
- `c`: affected by shaft support, rubbing surfaces, bearing/bushing fit, and servo gear friction
- `k`: affected by printed-frame stiffness, cable routing, and gravity coupling
- `tau_disturbance`: introduced by wire preload, misalignment, fastener preload, and bench motion

## Part List

| Part file | Function | Recommended print orientation | Physical rationale |
| --- | --- | --- | --- |
| `parts/base_plate.scad` | Rigid bench reference and clamp/fastener platform | flat on bed | The base should not flex or rock, because base motion appears as false gimbal motion in IMU data. |
| `parts/yaw_servo_mount.scad` | Holds the base-mounted yaw servo | flat with slots in XY plane | Slotted holes reduce alignment-induced side load, which reduces artificial friction and hysteresis. |
| `parts/outer_yaw_frame.scad` | Carries pitch axis and moving subsystem | back face on bed if possible | Frame stiffness affects `k`; flex can produce slow settling that looks like poor controller tuning. |
| `parts/pitch_servo_mount.scad` | Holds pitch actuator relative to outer frame | flat with attachment ears down | The pitch servo mount controls input-axis alignment and should not preload the pitch shaft. |
| `parts/inner_pitch_carrier.scad` | Carries mock nozzle and IMU | orient for strong shaft features | This is moving mass; compact geometry reduces `I_pitch` and improves transient response. |
| `parts/mock_nozzle.scad` | Visible nozzle surrogate and inertial load | vertical for circularity or horizontal for quick fit check | Hollowed geometry reduces pitch inertia while preserving visual scale for video. |
| `parts/hard_stop_block.scad` | Mechanical overtravel protection | flat on bed | Stops protect against calibration/software faults and keep motion within the test envelope. |
| `parts/wire_strain_relief_clip.scad` | Captures moving wires near rotation axes | flat on bed | Reduces wire stiffness acting as an unmodeled torsion spring. |

## Why Individual STLs Matter

A single combined STL is useful for visual review, but it is not a proper manufacturing package. Printing parts separately allows:

- different print orientations for strength
- local infill/wall changes near screw holes
- easier replacement after a failure
- part-by-part fit checks against real servos and fasteners
- cleaner revision history when one weak part changes

This is also better engineering evidence. A recruiter can see that the design is being treated as hardware with tolerances, load paths, and test consequences rather than as a decorative 3D model.

## Initial Export Targets

Future exported Rev A STLs should go in:

```text
cad/exports/rev_a_parts/
```

Recommended names:

```text
base_plate.stl
yaw_servo_mount.stl
outer_yaw_frame.stl
pitch_servo_mount.stl
inner_pitch_carrier.stl
mock_nozzle.stl
hard_stop_block.stl
wire_strain_relief_clip.stl
```

## Fit-Check Sequence

Before printing the full assembly:

1. Print `yaw_servo_mount.scad` as a small fit check.
2. Verify HS-625MG body, screw clearance, and slot alignment.
3. Print `pitch_servo_mount.scad` and check attachment concept.
4. Print `inner_pitch_carrier.scad` and mock nozzle to verify moving-mass envelope.
5. Assemble without power and sweep by hand through `+/-10 deg`.
6. Verify hard stops engage near `+/-15 deg`.
7. Route wires through strain-relief clips and repeat the manual sweep.

## What To Measure After Printing

| Measurement | Why it matters |
| --- | --- |
| pitch carrier + nozzle mass | Updates `I_pitch` and gravity moment. |
| yaw frame + pitch subsystem mass | Updates `I_yaw` and servo torque margin. |
| center-of-mass offset from each axis | Predicts steady gravity bias torque. |
| free-play at nozzle tip | Estimates backlash/compliance before closed-loop tests. |
| manual return-to-neutral repeatability | Identifies friction and cable preload. |
| hard-stop angle | Confirms mechanical protection outside firmware limit. |

These measurements close the loop between CAD assumptions and physical hardware behavior.
