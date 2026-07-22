# Rev A Part Export Log

Export date: `2026-07-21`

Renderer:

```text
OpenSCAD 2021.01
```

Command pattern:

```text
/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD \
  -o cad/exports/rev_a_parts/<part>.stl \
  cad/parts/<part>.scad
```

## Exported Parts

| STL | Source `.scad` | Render result |
| --- | --- | --- |
| `base_plate.stl` | `cad/parts/base_plate.scad` | OpenSCAD render completed, simple 3D object |
| `yaw_servo_mount.stl` | `cad/parts/yaw_servo_mount.scad` | OpenSCAD render completed, simple 3D object |
| `outer_yaw_frame.stl` | `cad/parts/outer_yaw_frame.scad` | OpenSCAD render completed, simple 3D object |
| `pitch_servo_mount.stl` | `cad/parts/pitch_servo_mount.scad` | OpenSCAD render completed, simple 3D object |
| `inner_pitch_carrier.stl` | `cad/parts/inner_pitch_carrier.scad` | OpenSCAD render completed, simple 3D object |
| `mock_nozzle.stl` | `cad/parts/mock_nozzle.scad` | OpenSCAD render completed, simple 3D object |
| `hard_stop_block.stl` | `cad/parts/hard_stop_block.scad` | OpenSCAD render completed, simple 3D object |
| `wire_strain_relief_clip.stl` | `cad/parts/wire_strain_relief_clip.scad` | OpenSCAD render completed, simple 3D object |

## Engineering Interpretation

These STLs are **Rev A print-review exports**, not final released manufacturing drawings. They prove that the separated CAD part files render successfully and can be opened in a slicer for first fit checks.

The next physical validation step is not controller tuning. It is dimensional and mechanical verification:

- servo body fit inside slotted mounts
- screw and slot clearance
- shaft/bushing fit
- hard-stop angle
- wire strain relief through `+/-10 deg` motion
- moving mass and center-of-mass measurement

This preserves the design-build-test chain:

```text
CAD assumption -> printed part -> measured fit/mass/clearance -> Rev B update
```

The control model depends on those measurements because the printed geometry sets inertia, compliance, friction, and disturbance torques.
