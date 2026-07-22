# Rev A Inspection Checklist

## Objective

Verify that the printed parts, servos, and assembled mechanism match the CAD and dynamic assumptions closely enough for first powered testing.

Inspection is part of the engineering model. A dimensional error is not just a manufacturing issue; it can change inertia, friction, backlash, stiffness, hard-stop margin, or sensor alignment.

## Incoming Hardware Inspection

Complete before modifying CAD or assembling the gimbal.

| Item | CAD / expected value | Measured value | Pass / investigate | Notes |
| --- | ---: | ---: | --- | --- |
| HS-625MG length | `40.6 mm` |  |  |  |
| HS-625MG width | `19.8 mm` |  |  |  |
| HS-625MG height | `37.8 mm` |  |  |  |
| Servo mounting ear span, X | `49.5 mm` placeholder |  |  | verify on arrival |
| Servo mounting ear span, Y | `27.5 mm` placeholder |  |  | verify on arrival |
| Servo horn usable radius | TBD from horn package |  |  | affects linkage / angle scale |
| Servo spline fit | expected compatible with included horn |  |  | check slop |
| BNO085 board length | vendor nominal |  |  | affects mount |
| BNO085 board width | vendor nominal |  |  | affects mount |

Physical interpretation:

- Servo body mismatch changes mount preload and alignment. If the servo is squeezed or cocked in the mount, the output shaft can carry side load, increasing friction and hysteresis.
- Horn radius affects commanded mechanical angle per servo rotation if a linkage is used. Even for direct visual motion, horn indexing affects neutral bias.
- Spline or horn slop creates backlash. In data, this appears as approach-direction dependence and hysteresis bias.

## Printed Part Inspection

| Part | Check | Pass / investigate | Notes |
| --- | --- | --- | --- |
| base plate | lies flat on bench |  | base rocking contaminates measurements |
| base plate | mounting holes clear |  | avoid drilling that shifts alignment |
| yaw servo mount | servo fits without forcing |  | forced fit adds preload |
| yaw servo mount | slots usable |  | alignment adjustment available |
| outer yaw frame | no visible warping |  | yaw inertia/stiffness assumption preserved |
| outer yaw frame | pitch-axis supports aligned |  | prevents pitch binding |
| pitch servo mount | servo fits without forcing |  | avoids shaft side load |
| inner pitch carrier | nozzle mount aligned |  | preserves pitch balance |
| mock nozzle | printed mass acceptable |  | affects `I_pitch` and `I_yaw` |
| hard-stop blocks | stop faces intact |  | impact/load path |
| strain-relief clips | usable without wire pinch |  | reduce cable torque bias |

Physical interpretation:

- Warped or misaligned frames reduce the quality of the plant identification test. The response may show extra damping/friction or stiffness that comes from print error rather than the intended gimbal architecture.
- Printed mass affects inertia. If the nozzle or carrier mass differs significantly from estimate, update the pre-hardware model before comparing measured response.
- Hole cleanup should be recorded. Removing material or shifting holes changes alignment and may create a hidden Rev A modification.

## Assembly Inspection

| Check | Requirement | Pass / investigate | Notes |
| --- | --- | --- | --- |
| yaw axis manual sweep | free motion through `+/-10 deg` |  | no servo power |
| pitch axis manual sweep | free motion through `+/-10 deg` |  | no servo power |
| yaw hard stop angle | engages after firmware range |  | target about `+/-15 deg` |
| pitch hard stop angle | engages after firmware range |  | target about `+/-15 deg` |
| neutral nozzle alignment | near mechanical zero |  | before closed-loop test |
| wire slack | no tension through motion range |  | avoid spring torque |
| IMU alignment | visibly aligned with gimbal axes |  | sign convention |
| fastener preload | no binding after tightening |  | check before/after torque |
| base stability | no rocking or sliding |  | clamp if needed |

Physical interpretation:

- If an axis moves freely before tightening but binds after tightening, the issue is preload or alignment, not servo authority.
- If hard stops engage too close to the firmware range, transient overshoot or calibration error can cause repeated impacts. That introduces nonlinear impact dynamics and can damage servo gears.
- Wire tension creates a restoring or bias moment. In the plant model it appears as `tau_disturbance` and possibly extra `k theta`.

## Backlash And Hysteresis Hand Check

Before powered tests, gently move each axis by hand near neutral.

| Axis | Free play at nozzle tip | Approx angular free play | Pass / investigate | Notes |
| --- | ---: | ---: | --- | --- |
| pitch |  |  |  |  |
| yaw |  |  |  |  |

Use:

```text
theta_free_play ~= x_tip / L_nozzle
```

for small angles, where `x_tip` is lateral free play at the nozzle tip and `L_nozzle` is the distance from rotation axis to tip.

Physical interpretation:

- Backlash creates a dead zone where servo output changes before the nozzle angle changes. In step-response data, this increases response delay and hysteresis bias.
- Backlash is not well represented by the first linear model. If hand-measured free play is large, the first report should explicitly state that Rev A is dominated by nonlinear joint clearance.

## Mass Properties Update

Record printed masses before assembly if possible.

| Component | Estimated mass | Measured mass | Update needed? |
| --- | ---: | ---: | --- |
| inner pitch carrier |  |  |  |
| mock nozzle |  |  |  |
| pitch servo |  |  |  |
| outer yaw frame |  |  |  |
| hardware / fasteners |  |  |  |

Physical interpretation:

- Pitch inertia is driven by the pitch carrier, nozzle, IMU, and hardware about the pitch axis.
- Yaw inertia includes the entire pitch assembly plus the yaw frame. This is why yaw response is expected to be slower.
- A mass update should be reflected in `data/examples/prehardware_model_parameters.json` or documented as a known prediction error before hardware comparison.

## Inspection Outcome

| Decision | Criteria |
| --- | --- |
| proceed to servo-neutral test | all safety-critical checks pass, no binding through command range |
| proceed with caution | minor dimensional mismatch, but no hard-stop or binding issue |
| stop and rework | servo does not fit, axis binds, hard stops unsafe, wiring tension high, or IMU cannot mount rigidly |

Inspection notes should be copied into the first test report so the measured response can be interpreted in context.
