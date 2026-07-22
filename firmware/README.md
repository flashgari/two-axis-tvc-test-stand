# Firmware

Prototype 1 firmware targets a Raspberry Pi Pico-class RP2040 board running MicroPython.

The first firmware milestone is safe open-loop bring-up:

```text
servo neutral -> limited sweep -> CSV telemetry -> IMU readout -> step response -> PID
```

## Current Firmware Files

| File | Purpose |
| --- | --- |
| `src/main.py` | Main Pico loop and selected test mode. |
| `src/config.py` | Physical constants, pins, loop rate, PWM limits, and command envelope. |
| `src/actuators.py` | Angle clamp, angle-to-PWM mapping, and servo command class. |
| `src/profiles.py` | Neutral, sweep, and step command profiles. |
| `src/imu_bno085.py` | BNO085 detection/telemetry placeholder. |
| `src/telemetry.py` | CSV header and row formatting. |
| `tests/` | Host-side checks for command limits and profiles. |

## Safety Defaults

The default mode in `src/main.py` is:

```python
MODE = "neutral"
```

Do not change to sweep or step modes until:

- servos have external `5 V` power
- servo supply ground and Pico ground are common
- the gimbal can move by hand through `+/-10 deg`
- hard stops are installed outside the firmware limit
- the mechanism is clamped or weighted on the bench

## Command Modes

Valid modes:

```text
neutral
sweep_pitch
sweep_yaw
step_pitch
step_yaw
```

The firmware clamps all angle commands to:

```text
+/-10 deg
```

The mechanical hard-stop target remains:

```text
about +/-15 deg
```

## Telemetry

The firmware streams CSV over USB serial:

```text
time_ms,mode,pitch_cmd_deg,yaw_cmd_deg,pitch_pwm_us,yaw_pwm_us,imu_present,quat_w,quat_x,quat_y,quat_z,gyro_x_dps,gyro_y_dps,gyro_z_dps
```

The BNO085 quaternion/rate fields are currently placeholders until the sensor driver is installed. The telemetry columns are defined now so future analysis scripts will not need to change format.

## Physical Interpretation

Servo PWM is an actuator input, not a guaranteed gimbal angle. The real plant is:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The firmware controls the `tau_servo` side indirectly through PWM pulse width. The measured IMU response will show the real effects of servo deadband, gear backlash, finite speed, structural compliance, and cable-induced bias.

That is why the first firmware milestone is open-loop telemetry, not immediate closed-loop PID. Before tuning a controller, the actuator and mechanism must be characterized.

## Host-Side Test

From the repo root:

```bash
python3 -m unittest discover firmware/tests
```

These tests verify that the angle-to-PWM mapping clamps commands before they can exceed the Rev A firmware envelope.
