# CAD Baseline

CAD files, exported drawings, and manufacturing notes live here.

## Prototype 1 Baseline

Prototype 1 uses two Hitec HS-625MG metal-gear servos and a 3D printed nested gimbal layout.

![Prototype 1 CAD baseline](exports/prototype1_cad_baseline.svg)

| File | Purpose |
| --- | --- |
| `prototype1_parameters.md` | Traceable dimensional assumptions, servo specs, axis convention, and quantities to verify. |
| `prototype1_gimbal_baseline.scad` | Parametric OpenSCAD first-pass model. |
| `prototype1_cad_review.md` | CAD design intent, physical rationale, review checklist, and expected Rev A failure modes. |
| `rev_a_mass_inertia_estimate.md` | First-pass moving mass, center-of-mass, gravity moment, and inertia estimates. |
| `rev_a_print_and_assembly_plan.md` | Printable part breakdown, assembly order, inspection checks, and physics rationale. |
| `exports/prototype1_cad_baseline.svg` | Static layout preview for GitHub/recruiter review. |
| `exports/prototype1_gimbal_baseline.stl` | OpenSCAD-rendered review STL of the combined layout assembly. |

## Export Status

The combined layout model has been rendered in OpenSCAD and exported as `exports/prototype1_gimbal_baseline.stl`.

This STL is **review evidence**, not a final print package. It proves that the parametric CAD baseline renders as a valid 3D object, but the assembly still needs to be split into manufacturing parts before printing:

- base plate
- yaw servo mount
- outer yaw frame
- pitch servo mount
- inner pitch/nozzle carrier
- mock nozzle
- hard-stop blocks
- wire strain-relief clips

The physical reason for separating the parts is that each component has a different print orientation, stiffness requirement, and failure mode. For example, servo mounts need strong screw-hole walls, the pitch carrier needs low moving inertia, and strain-relief clips need to control wire-induced torque without adding unnecessary mass to the moving body.

First CAD revision should include:

- fixed base
- outer gimbal frame
- inner gimbal frame
- mock nozzle
- actuator mounts
- linkage/horn geometry
- mechanical stops
- IMU mounting surface
- wire routing/strain relief

Design priorities:

1. Easy to print and assemble.
2. Easy to modify after first test.
3. Stiff enough for repeatable measurements.
4. Clear axis definitions for pitch and yaw.

## CAD Philosophy

The first model is deliberately parametric because the hardware will be measured after arrival. Servo body dimensions, horn thickness, spline fit, IMU board dimensions, moving mass, and center of mass should be updated before final printing.

The CAD is evaluated by how well it supports test data, not just how clean it looks. The stand should make it possible to identify actuator bandwidth, backlash, frame compliance, cable-induced bias, and IMU measurement issues from controlled experiments.

## Rev A Physical Model

The CAD package keeps the mechanical design tied to the rotational plant:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The Rev A mass estimate predicts:

| Axis | Moving mass estimate | Inertia estimate | Gravity moment estimate |
| --- | ---: | ---: | ---: |
| pitch | `73 g` | `3.0e-5 kg m^2` | `0.018 N m` |
| yaw | `200 g` | `3.0e-4 kg m^2` | `0.039 N m` |

These estimates suggest the first prototype should be limited more by servo speed, deadband, backlash, structural compliance, and wiring disturbances than by static torque. The hardware tests should therefore emphasize step response, hysteresis, steady-state bias, and repeatability.
