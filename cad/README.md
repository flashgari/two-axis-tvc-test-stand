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
| `exports/prototype1_cad_baseline.svg` | Static layout preview for GitHub/recruiter review. |

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
