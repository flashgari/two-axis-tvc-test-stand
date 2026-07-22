# Final Prototype 1 Purchase Package

Current check date: `2026-07-21`

This is the recommended first purchase package for Prototype 1. Prices and stock can change, so verify the cart immediately before ordering.

## Core Buy List

| Item | Qty | Current unit price | Current subtotal | Link | Why this exact item |
| --- | ---: | ---: | ---: | --- | --- |
| Raspberry Pi Pico H with pre-soldered headers | 1 | `$5.00` | `$5.00` | <https://www.adafruit.com/product/5525> | RP2040 is sufficient for `50-100 Hz` servo/IMU logging; headers reduce bring-up friction. |
| Adafruit BNO085 9-DOF orientation IMU breakout | 1 | `$24.95` | `$24.95` | <https://www.adafruit.com/product/4754> | Gives quaternion/rotation-vector telemetry for early attitude tests. |
| STEMMA QT/Qwiic JST-SH 4-pin cable, `100 mm` | 1 | `$0.95` | `$0.95` | <https://www.adafruit.com/product/4210> | Reduces I2C wiring mistakes and keeps IMU harness compact. |
| Hitec HS-625MG metal-gear PWM servo | 2 | `$43.99` | `$87.98` | <https://www.hiteccs.com/actuators/product-details/HS-625MG> | Traceable torque, speed, deadband, dimensions, mass, and 24T spline. |
| Adafruit `5 V`, `4 A` switching supply | 1 | `$14.95` | `$14.95` | <https://www.adafruit.com/product/1466> | Separate servo power prevents Pico brownout and corrupt telemetry. |
| Female `2.1 mm` DC jack to screw terminal | 1 | `$2.00` | `$2.00` | <https://www.adafruit.com/product/368> | Clean way to distribute the servo supply without cutting the power cable. |

Core subtotal:

```text
$135.83 before tax and shipping
```

## Local/Generic Hardware

These items can be bought from Amazon, McMaster, a local hardware store, or campus/makerspace stock. Exact dimensions should be finalized after the first servo fit check.

| Item | Qty | Planning cost | Notes |
| --- | ---: | ---: | --- |
| data-capable micro-USB cable | 1 | `$5-10` | Must support data, not charge-only. |
| jumper wire kit | 1 | `$6-12` | Male/female Dupont leads are useful for Pico/servo wiring. |
| small breadboard or protoboard | 1 | `$5-10` | For first wiring pass. |
| M3 screw assortment | 1 | `$8-15` | Needed for printed mounts and hard stops. |
| M3 heat-set inserts | optional | `$8-15` | Improves repeated assembly/disassembly. |
| PETG or PLA+ filament | available stock | `$0-25` | PETG preferred for toughness; PLA+ acceptable for fit checks. |
| small clamps or rubber feet | optional | `$5-10` | Keeps base from moving during tests. |
| `4 mm` shaft / small bushings or bearings | optional | `$5-20` | Depends on whether Rev A uses supported pitch shaft or direct-drive fit check. |

Estimated full first-build cost:

```text
$165-220 before tools
```

## Why This Package Is The Right First Purchase

The selected package maximizes measured engineering value per dollar. The expensive choice is the servo, not the microcontroller or IMU. That is intentional: the servo defines actuator bandwidth, backlash, deadband, torque margin, and fit geometry. A traceable HS-625MG actuator makes the CAD and test assumptions more defensible than a generic servo pack.

The test stand should be interpreted as a rotational plant:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

Each purchase affects that plant:

| Purchase | Physical effect |
| --- | --- |
| HS-625MG servos | set actuator speed, deadband, backlash, torque authority, and input lag |
| separate `5 V`, `4 A` supply | reduces voltage sag, reset risk, and command-dependent servo jitter |
| BNO085 IMU | provides measured attitude/rate so PWM input can be compared to actual motion |
| STEMMA/Qwiic cable | reduces wiring error and keeps the IMU harness repeatable |
| M3 hardware/inserts | determines mount stiffness and whether repeated assembly changes alignment |
| filament/print settings | determine frame compliance and therefore apparent damping/stiffness |

The purpose of Prototype 1 is not to prove that hobby servos are flight hardware. It is to personally design, build, test, and characterize a real electromechanical TVC plant.

## Do Not Buy Yet

Do not buy these until after the first fit checks:

- expensive bearing kits
- aluminum stock
- digital bus servos
- BLDC gimbal motors
- custom PCBs
- extra sensors beyond the BNO085

Those could become Rev B upgrades, but buying them now would blur the first-build scope.

## Pre-Arrival Work

Before parts arrive:

1. Slice the Rev A STL files in `cad/exports/rev_a_parts/`.
2. Print only the yaw servo mount as a first fit coupon.
3. Prepare MicroPython on the Pico.
4. Keep `firmware/src/main.py` in `MODE = "neutral"`.
5. Confirm the serial logger command works on the laptop.
6. Set up a folder for dated hardware logs.

## First Measurement After Parts Arrive

Before powered motion, measure:

- actual HS-625MG body dimensions
- mounting-ear hole spacing
- horn thickness and spline fit
- servo wire exit location
- printed mount slot fit
- moving pitch carrier/nozzle mass
- center-of-mass offset from pitch and yaw axes

These measurements update the CAD assumptions and the mass/inertia estimate before Rev A is treated as a real test article.
