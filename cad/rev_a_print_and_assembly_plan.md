# Rev A Print And Assembly Plan

## Purpose

Rev A is the first printable hardware configuration. Its purpose is to create a testable two-axis plant, not a final optimized mechanism. Every printed feature should either support measurement quality, protect hardware, or make the next iteration easier.

## Part Breakdown

| Part | Function | Print priority |
| --- | --- | --- |
| base plate | supports the full stand and provides clamp/fastener points | high |
| yaw servo mount | holds base-mounted yaw actuator | high |
| outer yaw frame | carries pitch axis and moving pitch subsystem | high |
| pitch servo mount | holds pitch actuator relative to outer frame | high |
| inner pitch carrier | carries mock nozzle and IMU | high |
| mock nozzle | visible moving mass for test videos and inertia estimate | medium |
| hard-stop blocks | mechanical overtravel protection | high |
| wire strain-relief clips | reduce cable-induced torque | high |

## Mechanical Choices And Physical Rationale

### Slotted Servo Mounts

Servo mounting holes are slotted in the CAD baseline.

Physical reason:

```text
misalignment -> side load / binding -> friction and hysteresis -> distorted step response
```

Slots allow the servo body to be aligned after printing. This reduces artificial friction and makes the measured actuator response more representative of the servo/gimbal system rather than printer tolerance error.

### Supported Pitch Shaft

Rev A includes a supported shaft/bearing reference for the pitch axis.

Physical reason:

```text
unsupported servo output shaft -> bending load -> gear friction/backlash growth
```

The servo should command angular position, not carry avoidable structural bending load. A supported shaft or bushing path helps separate actuation from structural support. If Rev A uses direct drive without a separate bearing, that limitation must be documented and tested.

### Hard Stops Outside Firmware Limits

Rev A uses:

```text
firmware command limit: +/-10 deg
mechanical hard stop: about +/-15 deg
```

Physical reason:

```text
calibration error or software fault -> overtravel -> servo/linkage damage
```

Hard stops should engage before the servo or linkage reaches a damaging internal limit. The gap between `10 deg` and `15 deg` provides tolerance for calibration and transient overshoot.

### IMU On Moving Carrier

The IMU is mounted on the pitch/nozzle carrier.

Physical reason:

```text
sensor on fixed base -> measures wrong state for feedback
sensor on moving body -> measures controlled output
```

This makes the feedback signal physically meaningful. The trade is that vibration and cable routing become more important, so the IMU pad should be stiff and the harness should be strain-relieved.

### Wire Slack Near Rotation Axis

Moving wires should loop near the rotation axes with slack.

Physical reason:

```text
tight wire harness -> torsional spring -> bias torque and apparent stiffness
```

If wire stiffness dominates the restoring moment, the controller will appear to be controlling the gimbal when it is partly fighting the harness. That would corrupt the actuator characterization.

## Rev A Print Settings

Initial recommendation:

| Setting | Baseline |
| --- | --- |
| Material | PETG preferred; PLA+ acceptable for first fit check |
| Layer height | `0.20 mm` |
| Perimeters/walls | `4` |
| Infill | `35-50%` |
| Top/bottom layers | `5+` |
| Servo mount region | increase walls or local modifier if available |
| Heat-set inserts | recommended for repeated assembly |

These are starting settings, not final manufacturing requirements. If the first step-response test shows structural flex or slow settling, increase stiffness before changing the controller.

## Assembly Order

1. Print base plate and servo-mount test coupons first.
2. Fit HS-625MG body into mount and verify slot alignment.
3. Install yaw servo and confirm unobstructed horn motion.
4. Assemble outer yaw frame.
5. Install pitch shaft/bushing or direct-drive interface.
6. Install pitch servo and inner carrier.
7. Mount mock nozzle and IMU pad.
8. Add wire strain relief before powered motion.
9. Manually sweep both axes through `+/-10 deg`.
10. Verify mechanical stops engage before servo/linkage binding.

## Inspection Before Power

- no servo horn contacts printed frame through `+/-10 deg`
- wires do not tighten through the motion range
- hard stops are not contacted during normal command range
- IMU board is mounted rigidly and visibly aligned
- base does not rock on the bench
- fasteners do not preload the gimbal asymmetrically

## Expected Rev A Test Consequences

The first print will likely have measurable nonidealities. The point is to capture them:

| Observation | Likely physical cause | Design response |
| --- | --- | --- |
| different neutral angle after positive vs negative approach | gear backlash or horn slop | quantify hysteresis, improve horn/interface fit |
| slow settling after command | frame flex, servo lag, or low damping | stiffen frame, reduce moving mass, retune PID |
| steady bias angle | gravity CM offset or wire preload | rebalance carrier, reroute wires |
| high-frequency IMU noise during motion | vibration or loose sensor mount | stiffen IMU pad, add filtering |
| servo jitter | power sag, signal noise, or deadband | improve power distribution, log voltage if possible |

This is the design-build-test loop the project is meant to demonstrate.
