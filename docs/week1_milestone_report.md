# Week 1 Milestone Report

## Objective

Select the Prototype 1 hardware architecture and define the first mechanical/electrical design baseline before purchasing parts or starting CAD.

## Decision

Prototype 1 will use the low-cost Option A architecture:

| Subsystem | Selection |
| --- | --- |
| Microcontroller | Raspberry Pi Pico-class RP2040 board |
| IMU | BNO085-class fused IMU breakout |
| Actuators | Two metal-gear PWM servos |
| Power | External regulated `5-6 V` servo supply |
| Structure | 3D printed PLA+/PETG gimbal |
| Control | PID first, model-based comparison later |

## Why This Is The Right First Prototype

The project goal is to demonstrate a complete hardware design-build-test loop. Prototype 1 should therefore minimize bring-up risk and cost while still producing meaningful engineering data.

The Pico-class microcontroller is inexpensive and sufficient for:

- two PWM actuator outputs
- I2C IMU communication
- `50-100 Hz` control loop
- USB serial CSV telemetry

The BNO085-class IMU reduces early attitude-estimation workload so the first prototype can reach closed-loop hardware testing faster. Raw gyro/accel channels should still be logged where available to preserve sensor-analysis depth.

Metal-gear PWM servos are not perfect actuators. They have backlash, finite bandwidth, deadband, and current spikes. That is acceptable because the first hardware milestone is to measure and document those limitations, not hide them.

The selected architecture is cheap, but it still captures the main controls physics of a TVC mechanism. The gimbal is a rotational plant with inertia, damping, stiffness/compliance, saturation, and disturbance torques. The embedded controller will command nozzle angle, the servos will impose actuator dynamics and deadband, and the IMU will measure the resulting attitude/rate response with its own latency and filtering. Those are exactly the effects that determine whether a thrust-vectoring system has enough bandwidth and phase margin to reject disturbances.

This first prototype is therefore not trying to prove that hobby hardware is flight hardware. It is trying to prove that the mechanism can be designed, built, instrumented, tested, and improved using measured data. That is the portfolio value.

## Cost Estimate

Expected Prototype 1 cost:

```text
about $85-150 before tools
```

The exact total depends mostly on servo selection, fasteners/bearings, and whether headers/cables/power hardware are already available.

## Actuator Sizing Result

Using a conservative static estimate:

```text
m = 0.20 kg
r = 0.04 m
tau_gravity = m g r = 0.078 N m ~= 0.80 kg-cm
```

With a `3x` margin:

```text
tau_servo,target >= 2.4 kg-cm
```

Prototype 1 should select servos with at least `5 kg-cm` stall torque to leave margin for friction, wiring drag, printed-frame flex, and dynamic motion.

This sizing result should be read as a lower-bound screen, not a final actuator certification. Static stall torque only says the servo should hold the moving mass against gravity. Closed-loop TVC performance also depends on dynamic response:

```text
I_axis theta_ddot + c theta_dot + k theta ~= tau_servo + tau_disturbance
```

where `I_axis` is the moving assembly inertia, `c` represents effective damping, `k` represents structural/cable stiffness or gravity coupling, and `tau_disturbance` includes wire drag, friction, and off-axis loads. The first step-response tests will use measured rise time, overshoot, settling time, and steady-state bias to identify whether the limiting factor is torque, bandwidth, backlash, compliance, or sensor filtering.

## CAD Baseline

The first CAD concept will use:

- fixed base
- outer gimbal frame
- inner nozzle carrier
- mock nozzle
- direct servo drive if packaging allows
- mechanical hard stops around `+/-15 deg`
- firmware command limits around `+/-10 deg`
- IMU mounted on the moving nozzle carrier
- visible sensor-axis markings
- wire strain relief

## Wiring Baseline

The electrical architecture is:

```text
USB laptop -> Pico-class microcontroller
Pico I2C -> BNO085 IMU
Pico PWM -> pitch/yaw servos
external 5-6 V supply -> servo power
servo supply ground == microcontroller ground
```

Servos will not be powered from the microcontroller USB rail.

The separate servo supply is an engineering requirement, not just a wiring preference. Servo current spikes can pull down the logic rail, reset the microcontroller, corrupt telemetry, or create IMU noise during motion. A common ground is still required so the PWM signal has a valid voltage reference at the servo input.

## Next Work

1. Choose exact vendor links and servo model.
2. Confirm servo dimensions and horn geometry.
3. Create first CAD assembly.
4. Create firmware skeleton for PWM neutral, IMU readout, and CSV telemetry.
5. Run actuator neutral/range tests once hardware arrives.

## Portfolio Relevance

This milestone turns the project from an idea into an engineering baseline. It records design choices, cost reasoning, actuator sizing, wiring constraints, and CAD requirements before hardware is purchased.

The key result from Week 1 is that the first build has a defensible requirements chain: target gimbal motion leads to actuator torque screening, actuator choice leads to power and wiring constraints, CAD geometry determines inertia and disturbance moments, and sensor placement determines what state is actually measured for feedback. That chain is what makes the project read like an aerospace controls build instead of a parts assembly.
