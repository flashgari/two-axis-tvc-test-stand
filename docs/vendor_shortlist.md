# Vendor Shortlist And Purchase Decision

Current check date: `2026-07-21`

This document converts the Prototype 1 architecture into a buyable parts list. Prices and availability should be checked again immediately before ordering.

## Selected First Purchase

Prototype 1 will use the traceable-servo path. The strict-budget servo path is retained below only as a rejected lower-cost alternative.

| Subsystem | Recommended part | Qty | Current reference price | Link | Engineering reason |
| --- | --- | ---: | ---: | --- | --- |
| Microcontroller | Raspberry Pi Pico H, pre-soldered headers | 1 | `$5.00` | <https://www.adafruit.com/product/5525> | RP2040 has enough PWM, I2C, timing, and USB serial bandwidth for a `50-100 Hz` TVC test stand controller. Headers reduce bring-up time. |
| IMU | Adafruit BNO085 9-DOF orientation breakout | 1 | `$24.95` | <https://www.adafruit.com/product/4754> | Provides quaternion/rotation-vector output for rapid first closed-loop tests while still allowing raw gyro/accel logging where available. |
| I2C cable | STEMMA QT / Qwiic JST SH cable, `100-200 mm` | 1 | about `$0.95-1.25` | <https://www.adafruit.com/product/4399> | Reduces wiring errors on the IMU interface and keeps the sensor harness clean. |
| Servo power | Regulated `5 V`, `4 A` supply | 1 | `$14.95` | <https://www.adafruit.com/product/1466> | Two servos can draw large transient current. A separate supply protects the microcontroller and telemetry from brownouts. |
| Power adapter | Female `2.1 mm` jack to screw terminal | 1 | `$2.00` | <https://www.adafruit.com/product/368> | Provides a clean way to distribute servo power without cutting the wall supply cable. |

## Servo Decision

The servo choice is the main cost/quality trade. The selected decision is Path A: two Hitec HS-625MG standard metal-gear servos.

### Path A: Traceable Servo, Stronger Documentation

| Part | Qty | Current reference price | Link | Key specs |
| --- | ---: | ---: | --- | --- |
| ServoCity Hitec HS-625MG standard metal-gear servo | 2 | `$43.99` each | <https://www.servocity.com/hs-625mg-servo/> | `5.5 kg-cm` at `4.8 V`, `6.8 kg-cm` at `6.0 V`, about `0.15 s/60 deg` at `6.0 V`, standard-size package |

This is the selected path. The benefit is that torque, speed, deadband, current, spline, mass, and dimensions are published by the vendor, which makes the CAD model and test-plan assumptions easier to defend.

Estimated electronics/servo subtotal:

```text
5.00 + 24.95 + 1.25 + 14.95 + 2.00 + 2*43.99 ~= $136.13
```

After fasteners, bearings, filament, jumpers, and shipping, this likely becomes about `$165-220`.

### Rejected Alternative: Strict-Budget Servo, Lower Cost

| Part family | Qty | Typical low-cost route | Key specs to verify before buying |
| --- | ---: | --- | --- |
| MG996R/MG995-class metal-gear PWM servo pack | 2 plus spares | Amazon/eBay/robotics suppliers | `>= 5 kg-cm` stall torque at `5-6 V`, standard-size `~40 x 20 x 43 mm`, metal gears, included horns, stall current estimate |

This path is rejected for Prototype 1 because generic servo listings can have inconsistent specs, clone variation, and weaker documentation. It would lower the cost, but it would make the first CAD model and test report less defensible.

Expected strict-budget subtotal:

```text
electronics + servo pack ~= $75-120 before mechanical hardware and shipping
```

Path B remains a fallback only if the budget changes later.

## Current Decision

Prototype 1 will buy two Hitec HS-625MG servos. This is the cleaner portfolio path because the first CAD and test report can reference traceable actuator specifications instead of relying on generic marketplace claims.

The actuator is still not assumed ideal. Even with a traceable servo, the hardware campaign must measure backlash, deadband, response time, steady-state error, and repeatability.

## CAD Inputs To Capture Before Modeling

Before the first CAD assembly is finalized, record:

| Quantity | Why it matters |
| --- | --- |
| Servo body dimensions | Determines mount geometry and gimbal spacing. |
| Output spline / horn geometry | Determines direct-drive interface and angular zero reference. |
| Servo mass | Adds to moving inertia if mounted on the moving frame. |
| Wire exit location | Affects cable routing and disturbance torque. |
| IMU board dimensions and mounting holes | Determines moving-body sensor placement. |
| Mock nozzle mass and center of mass | Determines gravity moment and required servo torque. |

## Upper-Division Physical Rationale

The first hardware purchase is not only a cost decision. It determines the physical plant that the controller sees:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo(theta_cmd, theta_dot, V_supply) + tau_disturbance
```

The servo contributes finite bandwidth, deadband, saturation, backlash, and voltage sensitivity. The printed gimbal contributes inertia, compliance, friction, and alignment error. The IMU contributes measurement noise, filter delay, and frame-alignment uncertainty. A successful first prototype is one where these effects are small enough to close the loop, but visible enough to measure and discuss.

That is why the purchase decision is documented before buying parts. The test results will later be interpreted against these assumptions instead of being treated as disconnected plots.
