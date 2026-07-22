# Rev A Mass, Center-Of-Mass, And Inertia Estimate

Current estimate date: `2026-07-21`

This document estimates the moving mass properties of Prototype 1 before hardware arrives. These values are first-pass engineering estimates, not final measured properties. After printing and assembly, the moving masses and center-of-mass offsets should be measured and this file should be updated.

## Why This Matters

The gimbal is a rotational dynamics problem. For each axis, the small-angle plant can be approximated as:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The CAD model directly sets the dominant mass-property terms:

- `I_axis`: rotational inertia of the moving gimbal/nozzle assembly
- `k`: effective stiffness from gravity coupling, printed-frame flex, and wire preload
- `tau_disturbance`: friction, cable drag, shaft misalignment, and off-axis weight

This is why CAD cannot be treated as just packaging. If the moving center of mass is far from the rotation axis, gravity creates a steady bias moment. If the mass is spread far from the axis, the same servo torque produces lower angular acceleration. If wires are routed tightly across the moving frame, they act like torsion springs and contaminate the controller response.

## Rev A Mass Budget

### Pitch Axis Moving Assembly

The pitch axis controls the inner carrier, mock nozzle, IMU board, local fasteners, horn/interface hardware, and moving wire segment.

| Component | Estimated mass |
| --- | ---: |
| printed inner pitch carrier | `30 g` |
| printed mock nozzle | `25 g` |
| BNO085 breakout | `5 g` |
| servo horn/interface hardware | `8 g` |
| moving wire slack | `5 g` |
| **pitch moving mass estimate** | **`73 g`** |

The previous actuator sizing used a deliberately conservative `0.20 kg` moving mass. The Rev A pitch estimate is lower, but the conservative sizing is still useful because it covers under-estimated print mass, extra hardware, and friction.

### Yaw Axis Moving Assembly

The yaw axis moves the pitch carrier/nozzle assembly plus the pitch servo, part of the outer frame, and wiring.

| Component | Estimated mass |
| --- | ---: |
| pitch moving assembly | `73 g` |
| pitch servo | `55 g` |
| printed outer yaw frame contribution | `45 g` |
| bearings/shafts/fasteners | `20 g` |
| moving wire slack | `7 g` |
| **yaw moving mass estimate** | **`200 g`** |

The yaw axis is expected to have larger inertia than pitch because it carries the pitch actuator and outer-frame hardware.

## Center-Of-Mass Offset Estimate

The static gravity moment is:

```text
tau_g = m g r
```

where `r` is the perpendicular offset between the rotation axis and the moving center of mass.

### Pitch Axis Gravity Bias

Using:

```text
m_pitch = 0.073 kg
r_pitch = 0.025 m
g = 9.81 m/s^2
```

gives:

```text
tau_g,pitch = 0.073 * 9.81 * 0.025
             = 0.0179 N m
             ~= 0.18 kg-cm
```

### Yaw Axis Gravity Bias

Using:

```text
m_yaw = 0.200 kg
r_yaw = 0.020 m
g = 9.81 m/s^2
```

gives:

```text
tau_g,yaw = 0.200 * 9.81 * 0.020
           = 0.0392 N m
           ~= 0.40 kg-cm
```

The HS-625MG servo is rated around `6.8 kg-cm` stall torque at `6.0 V`, so the static gravity torque estimate is far below stall torque. That does not mean the actuator is automatically adequate for closed-loop control. It only means the first CAD is not obviously torque-starved in static holding.

## Inertia Estimate

The inertial requirement is more important for transient control than the static gravity moment.

### Pitch Axis

Approximate the nozzle as a slender body with length `L = 0.085 m`, radius `r = 0.012 m`, and mass `m = 0.025 kg`. The transverse inertia estimate is:

```text
I_nozzle ~= (1/12) m (3 r^2 + L^2)
```

```text
I_nozzle ~= (1/12)(0.025)(3*0.012^2 + 0.085^2)
         ~= 1.6e-5 kg m^2
```

Adding the carrier, IMU, horn, fasteners, and wire slack gives a first-pass pitch-axis estimate:

```text
I_pitch ~= 3.0e-5 kg m^2
```

### Yaw Axis

The yaw axis carries more distributed mass. A coarse parallel-axis estimate is:

```text
I_yaw ~= sum(m_i r_i^2)
```

Using a representative radius of `0.040 m` for `0.150 kg` of moving mass plus local frame/shaft inertia:

```text
I_yaw ~= 0.150 * 0.040^2 + local terms
      ~= 2.4e-4 kg m^2 + local terms
```

Rev A working value:

```text
I_yaw ~= 3.0e-4 kg m^2
```

## Control-Relevant Interpretation

Servo stall torque at `6.0 V`:

```text
tau_stall ~= 6.8 kg-cm ~= 0.667 N m
```

A responsible design should not assume full stall torque is available for clean control. If only `20%` of stall torque is treated as useful transient control authority:

```text
tau_useful ~= 0.13 N m
```

Then the rough angular acceleration capability is:

```text
alpha_pitch ~= tau_useful / I_pitch
            ~= 0.13 / 3.0e-5
            ~= 4.3e3 rad/s^2
```

```text
alpha_yaw ~= tau_useful / I_yaw
          ~= 0.13 / 3.0e-4
          ~= 4.3e2 rad/s^2
```

These acceleration estimates are intentionally rough. They show that Rev A is likely limited by servo internal speed, deadband, backlash, and structural compliance rather than pure torque. That matches the expected hardware-test story: the first meaningful plots should focus on step-response lag, overshoot, steady-state error, hysteresis, and repeatability.

## CAD Implications

The Rev A CAD should preserve the following choices:

- keep the pitch carrier compact to reduce `I_pitch`
- avoid mounting unnecessary hardware on the pitch carrier
- mount the pitch servo so the yaw axis can carry it without excessive offset
- route IMU and servo wires with slack near the rotation axis
- use slotted servo mounts to reduce alignment-induced binding
- use mechanical hard stops outside the firmware command range

## Measurements Needed After Assembly

After parts arrive and the first print is assembled:

1. Weigh the pitch moving assembly.
2. Weigh the yaw moving assembly.
3. Balance each moving assembly to estimate center-of-mass offset.
4. Record actual servo horn geometry and linkage/direct-drive offset.
5. Repeat the gravity-torque estimate with measured values.
6. Use step-response data to infer whether the dominant limitation is inertia, servo lag, backlash, or compliance.

The portfolio value is in closing this loop: CAD estimate, physical build, measured data, and design iteration.
