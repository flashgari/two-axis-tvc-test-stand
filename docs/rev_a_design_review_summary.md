# Rev A Design Review Summary

## Review Objective

Assess whether Prototype 1 Rev A is ready to move from design artifacts to physical fabrication, calibration, and first measured step-response testing.

Rev A is intentionally a benchtop controls/mechanisms article, not a flight-like actuator. Its purpose is to generate measured plant behavior that can be compared against a pre-hardware dynamic prediction.

## Design Status

| Area | Status | Evidence |
| --- | --- | --- |
| Requirements | ready | two-axis range, command tracking, data logging, safety scope |
| Actuator selection | ready | Hitec HS-625MG selected for traceable dimensions/torque/speed |
| Electronics | ready | Pico-class controller, BNO085-class IMU, external servo supply |
| CAD baseline | ready for first print | parametric OpenSCAD assembly plus split printable STL exports |
| Firmware | ready for bring-up | neutral, sweep, step profile, PWM clamp, telemetry skeleton |
| Analysis | ready | CSV logging, metrics extraction, plotting, synthetic and pre-hardware examples |
| Test planning | ready | neutral procedure, calibration worksheet, log templates |
| Hardware data | pending | requires purchased parts and printed Rev A hardware |

## Key Physical Model

The gimbal is treated as a low-order rotational plant:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
delta_dot = (delta_cmd - delta) / tau_servo_lag
tau_servo = clamp(K_servo (delta - theta), -tau_limit, +tau_limit)
```

This model is deliberately simple enough to be identifiable from first hardware logs. Each term maps to a physical feature:

| Term | Physical source in Rev A |
| --- | --- |
| `I_axis` | printed moving mass, servo placement, nozzle carrier, pitch assembly carried by yaw |
| `c theta_dot` | servo geartrain friction, bearing losses, plastic flex damping, cable rubbing |
| `k theta` | frame compliance, wire preload stiffness, gravity-restoring/anti-restoring geometry |
| `tau_disturbance` | center-of-mass offset, horn indexing error, cable routing bias |
| `tau_servo_lag` | internal servo controller bandwidth, PWM update rate, mechanical response lag |
| `tau_limit` | useful dynamic torque, intentionally below datasheet stall torque |

## Design Strengths

1. **Traceable engineering chain:** Requirements, hardware selection, CAD, firmware, data logging, analysis, and test planning are connected instead of existing as isolated files.

2. **Falsifiable prediction before hardware:** The pre-hardware response model publishes assumptions before test data exists. This makes later deviations meaningful evidence rather than post-hoc explanation.

3. **Axis-specific physics:** Pitch and yaw are not assumed to behave identically. Yaw carries the pitch subsystem, so larger yaw inertia should produce slower response and potentially larger sensitivity to compliance/backlash.

4. **Safety-first bring-up:** The first powered procedure starts with servo horns removed, then progresses through neutral verification, limited sweep, and measured step tests.

5. **Data interpretation plan:** Step-response metrics are tied to physical causes such as actuator lag, friction, backlash, compliance, wire preload, sensor filtering, and voltage sag.

## Remaining Rev A Risks

| Risk | Why it matters physically | First test that exposes it |
| --- | --- | --- |
| Servo horn spline mismatch | creates neutral offset and trim moment | servo-neutral calibration |
| Printed frame compliance | reduces effective stiffness and can add phase lag/overshoot | pitch/yaw step response |
| Gear backlash or horn slop | creates approach-direction hysteresis not captured by linear model | `-5 -> +5 -> -5 deg` hysteresis test |
| Wire preload | adds a constant or weakly elastic disturbance torque | neutral repeatability and steady-state error |
| Servo supply droop | reduces available torque and speed during motion | step test with voltage logging |
| IMU sign/filter issue | can destabilize feedback or corrupt derivative estimate | hand-deflection sign and rate check |
| Bearing/bushing friction | consumes servo torque and slows rise time | measured rise time vs prediction |

## First Hardware Validation Plan

The first hardware campaign should proceed in this order:

1. Servo-neutral test with horns removed.
2. Horn indexing and mechanical-zero calibration.
3. IMU sign, zero, and rate verification.
4. `+/-2 deg` low-risk pitch and yaw step tests.
5. `+/-5 deg` pitch and yaw step tests for comparison with pre-hardware prediction.
6. Hysteresis tests using negative-to-positive and positive-to-negative approach paths.
7. Update model parameters from measured rise time, overshoot, settling time, steady-state error, and hysteresis bias.

## What Rev B Depends On

Rev B should not be designed by preference. It should be driven by measured failure mode:

| Measured result | Rev B design response |
| --- | --- |
| rise time much slower than predicted | reduce moving inertia, increase servo torque margin, reduce friction, improve supply stiffness |
| large steady-state error | rebalance moving assembly, reroute wires, refine horn indexing, add trim calibration |
| high overshoot/ringing | stiffen frame, shorten load paths, improve bearing support, reduce controller aggressiveness |
| large hysteresis bias | improve horn coupling, reduce slop, add better bearings/bushings, redesign joints |
| yaw much worse than predicted | reduce mass carried by yaw, move pitch servo closer to yaw axis, increase yaw actuator authority |
| noisy attitude/rate telemetry | improve IMU mounting, isolate vibration, check power noise, adjust filtering |

## Review Conclusion

Rev A is ready to proceed to purchase, printing, assembly, and first powered calibration. The design is not claimed to be final. It is a controlled first article intended to generate measured plant data.

The project will be strongest when the first hardware results are presented as:

```text
prediction -> measured response -> physical discrepancy -> design update
```

That loop demonstrates personally designed, built, and tested aerospace hardware with a controls-oriented engineering interpretation.
