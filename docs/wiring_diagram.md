# Wiring Diagram

## Prototype 1 Electrical Architecture

```text
USB laptop
  |
  | USB data + microcontroller power
  v
Raspberry Pi Pico-class microcontroller
  | I2C SDA/SCL
  v
BNO085 IMU

external 5-6 V servo supply
  | +5-6 V
  | GND --------------------+
  v                         |
pitch servo                 |
yaw servo                   |
                            |
microcontroller GND --------+

microcontroller PWM pin -> pitch servo signal
microcontroller PWM pin -> yaw servo signal
```

## Critical Rule

The servo supply and microcontroller must share ground:

```text
servo_supply_GND == microcontroller_GND
```

Without common ground, PWM signals do not have a valid reference and servo behavior can become erratic.

## Power Plan

| Load | Power source |
| --- | --- |
| Microcontroller | USB from laptop |
| IMU | Microcontroller `3.3 V` |
| Servos | External regulated `5-6 V` supply |

Do not power servos from the microcontroller `5 V`/USB rail. Servo current spikes can reset the board and corrupt data logs.

## Signal Plan

| Signal | Direction | Notes |
| --- | --- | --- |
| I2C SDA | microcontroller <-> IMU | Pullups usually provided by breakout |
| I2C SCL | microcontroller <-> IMU | Keep wires short for first prototype |
| Pitch PWM | microcontroller -> pitch servo | Firmware-limited command range |
| Yaw PWM | microcontroller -> yaw servo | Firmware-limited command range |
| USB serial | microcontroller -> laptop | CSV telemetry |

## Wiring Best Practices

- Keep servo power wires thicker than signal wires.
- Twist or bundle servo power/ground where practical.
- Route IMU wires away from moving joints.
- Strain-relieve all wires on the moving gimbal.
- Label pitch and yaw servo connectors.
- Add a reachable power switch or unplug point for the servo supply.

## Bring-Up Order

1. Connect microcontroller over USB only.
2. Confirm serial output.
3. Connect IMU and confirm readings.
4. Connect one servo with external supply.
5. Confirm neutral command only.
6. Add limited sweep.
7. Add second servo.
8. Enable logging.

## Failure Modes To Watch

| Symptom | Likely cause |
| --- | --- |
| Microcontroller resets when servo moves | Servo current sag/brownout |
| Servo jitters | Bad ground reference, noisy power, weak supply |
| IMU readings jump during servo motion | Vibration, wire tug, supply noise |
| Axis moves wrong direction | Sign convention mismatch |
| Servo hits hard stop | Calibration/firmware limit error |
