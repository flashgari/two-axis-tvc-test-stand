# Actuator Sizing

## Purpose

The actuator sizing goal is not to certify a flight actuator. It is to verify that the selected hobby servos have enough torque margin to move a lightweight mock nozzle/gimbal assembly during benchtop tests.

## Free-Body Model

Each servo must overcome:

```text
tau_required ~= tau_gravity + tau_inertia + tau_friction + tau_wire + margin
```

For a first-pass static estimate, gravity torque dominates if the gimbal mass center is offset from the rotation axis:

```text
tau_gravity = m g r
```

where:

- `m` is the moving mass supported by the axis
- `g` is gravitational acceleration
- `r` is the distance from rotation axis to moving center of mass

## Prototype 1 Assumptions

| Parameter | First-pass value |
| --- | ---: |
| Moving nozzle/gimbal mass | `0.10-0.20 kg` |
| CM offset from axis | `20-40 mm` |
| Max gimbal angle | `10-15 deg` |
| Desired torque margin | `>= 3x static gravity torque` |

## Static Torque Estimate

Conservative case:

```text
m = 0.20 kg
r = 0.04 m
g = 9.81 m/s^2
```

```text
tau_gravity = m g r
             = 0.20 * 9.81 * 0.04
             = 0.078 N m
```

Convert to kg-cm:

```text
1 kg-cm = 0.0981 N m
tau_gravity ~= 0.80 kg-cm
```

With `3x` margin:

```text
tau_servo,target >= 2.4 kg-cm
```

Most metal-gear hobby servos exceed this static torque level. The real questions become backlash, bandwidth, stiffness, and current draw, which must be measured.

## Dynamic Considerations

Dynamic torque is:

```text
tau_inertia = I_axis alpha
```

For a lightweight mock nozzle, this is expected to be smaller than servo capability during low-speed prototype tests. However, aggressive step commands can excite:

- servo deadband
- gear backlash
- printed-frame flex
- linkage compliance
- IMU vibration

This is why the first tests begin with small-angle, low-speed command profiles.

The gimbal should also be interpreted as a second-order rotational plant over the small-angle range:

```text
I_axis theta_ddot + c theta_dot + k theta ~= tau_servo + tau_disturbance
```

For Prototype 1, `I_axis` comes from the moving nozzle/carrier inertia, `c` is an effective damping term from bearings, gears, and servo internal control, and `k` represents any effective stiffness or restoring moment from cable loads, flexure, or gravity coupling. The exact coefficients are not known before hardware exists. The goal of the first step-response tests is to estimate the practical behavior of this plant from data: rise time, overshoot, settling time, repeatability, and steady-state bias.

This matters because closed-loop TVC performance depends on actuator authority and phase lag, not stall torque alone. A servo with a large advertised stall torque can still be a poor TVC actuator if its response is slow, if the output shaft has backlash, or if current sag causes command-dependent motion errors.

## Servo Selection Requirement

Prototype 1 servos should satisfy:

| Requirement | Target |
| --- | ---: |
| Stall torque | `>= 5 kg-cm` preferred |
| Gear type | metal gear |
| Control | standard PWM |
| Supply | `5-6 V` external |
| Quantity | 2 plus optional spare |

## Physical Interpretation

A servo can have enough static torque and still perform poorly for controls. TVC is a bandwidth and tracking problem, not only a strength problem. The important measured quantities will be:

- commanded vs measured angle
- step-response settling time
- overshoot
- deadband/backlash
- repeatability
- current-induced brownout risk

The sizing estimate only gets the prototype into a plausible torque range. The hardware tests decide whether the actuator is actually good enough.

The physical interpretation of the `>= 5 kg-cm` requirement is therefore conservative but not final. It says the actuator should not fail the first prototype for obvious static-torque reasons. The real acceptance evidence will come from measured closed-loop behavior: if the gimbal tracks a small command with low steady-state error, limited overshoot, and no servo brownout, then the actuator is adequate for the first test article. If it overshoots, hunts, chatters near neutral, or cannot reject small disturbances, those plots become the engineering justification for a higher-bandwidth actuator or a stiffer mechanical redesign.
