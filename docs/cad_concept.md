# CAD Concept

## Prototype 1 Mechanical Concept

The first CAD model will be a compact two-axis gimbal for a mock nozzle. The mechanism is a benchtop controls test article, so the design prioritizes access, stiffness, and iteration speed over flight-like packaging.

The CAD model is not just a visual deliverable. It defines the plant that the controller will later regulate: axis alignment, center-of-mass offset, moving inertia, friction sources, cable routing, hard-stop geometry, and sensor placement. Small mechanical choices directly affect the control data, so every CAD revision should be tied to a physical hypothesis that can be tested.

## Coordinate Convention

```text
base frame:
  +z = up
  +x = pitch direction reference
  +y = yaw direction reference

gimbal axes:
  outer frame = yaw axis
  inner frame = pitch axis
```

The exact naming can be adjusted during CAD, but the axis convention must be documented so test data matches the firmware sign convention.

## Major Parts

| Part | Function |
| --- | --- |
| Base plate | Holds the full stand rigidly on the bench |
| Outer gimbal frame | Carries one rotational axis |
| Inner gimbal/nozzle carrier | Carries the mock nozzle and IMU |
| Mock nozzle | Visual engine/nozzle surrogate with known approximate mass |
| Servo mounts | Hold pitch/yaw servos with adjustable alignment |
| Mechanical stops | Prevent overtravel beyond safe range |
| IMU platform | Places sensor near moving body with known orientation |
| Wire relief | Prevents cable drag from becoming a disturbance torque |

## Design Targets

| Feature | Target |
| --- | --- |
| Angular range | At least `+/-10 deg` both axes |
| Hard stops | `+/-15 deg` approximate mechanical limit |
| Fasteners | Common M3 or equivalent |
| Assembly | Removable actuator mounts and nozzle carrier |
| Print strategy | Avoid supports where possible |
| Sensor mount | Flat surface with repeatable orientation |

## Actuator Geometry

Prototype 1 can use one of two servo layouts:

### Direct Horn Layout

Servo horn directly rotates the gimbal axis.

Strength:

- simple
- fewer parts
- easy firmware mapping

Risk:

- axis alignment must be good
- servo backlash directly appears as gimbal backlash

### Linkage Layout

Servo horn drives the gimbal through a pushrod/link.

Strength:

- easier to package
- mechanical advantage can be tuned

Risk:

- linkage slop
- nonlinear angle mapping
- harder calibration

Recommended Prototype 1 direction: direct horn if mechanically feasible; linkage only if packaging forces it.

The direct-drive option is preferred for the first build because it keeps the kinematic mapping between servo angle and gimbal angle close to linear. That makes calibration and control interpretation cleaner. A linkage can be useful later, but it introduces angle-dependent mechanical advantage and additional compliance, so any controller comparison would have to account for that nonlinear input mapping.

## IMU Placement

The IMU should be mounted on the moving inner gimbal/nozzle carrier, not the fixed base. The sensor axes should be aligned with the documented gimbal axes as closely as possible.

Important:

- Record sensor orientation in CAD.
- Add a visible arrow or label for sensor `+x/+y`.
- Keep the IMU wire flexible and strain-relieved.

Mounting the IMU on the moving carrier means the measured attitude corresponds to the controlled output, not the fixed base. However, this also exposes the sensor to local vibration and cable-induced loads. The CAD should therefore place the IMU on a stiff region of the carrier and route wires so they do not add a hidden restoring torque or bias the neutral angle.

## Mechanical Stops

Mechanical stops should limit travel before the servo or linkage binds.

Initial target:

```text
firmware command limit: +/-10 deg
mechanical hard stop: about +/-15 deg
```

The gap between firmware limit and hard stop gives protection against calibration error.

## CAD Deliverables

First CAD milestone should produce:

- screenshot/render of full assembly
- exploded or annotated view
- axis convention figure
- approximate moving mass estimate
- hardware list for fasteners/bearings
- print orientation notes

## Known First-Prototype Risks

- printed-frame flex changes measured response
- servo backlash dominates tracking error
- wire drag biases neutral position
- IMU mount vibration contaminates rate measurements
- direct-drive geometry may not package cleanly

The first CAD revision should make these risks easy to inspect and modify.

These risks are expected, not embarrassing. A strong hardware portfolio project shows that the first design was instrumented well enough to identify the failure mode. For example, if measured attitude lags command even at low frequency, the likely cause may be servo bandwidth or sensor filtering. If the steady-state neutral angle changes after moving in opposite directions, backlash or cable preload is more likely. The CAD should make those effects observable instead of hiding them inside inaccessible geometry.
