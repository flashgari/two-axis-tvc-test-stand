# System Architecture

## High-Level Architecture

```text
USB host laptop
  | serial commands / telemetry
  v
microcontroller
  | PWM actuator commands
  | I2C/SPI IMU data
  v
two-axis gimbal test stand
  | measured angular response
  v
CSV logs and plots
```

## Subsystems

### Mechanical

Purpose: provide a rigid, adjustable two-axis gimbal for a mock nozzle.

Initial concept:

- fixed base plate
- outer pitch/yaw frame
- inner gimbal frame
- mock engine/nozzle cylinder
- two actuator linkages or direct servo horns
- mechanical hard stops
- IMU mount close to moving body

Key mechanical risks:

- backlash in servo gears/linkages
- flex in printed brackets
- axis misalignment
- wire drag applying unwanted torque
- insufficient base stiffness

### Electronics

Purpose: command actuators, read sensor data, and stream telemetry.

Initial architecture:

- microcontroller with hardware PWM and fast serial logging
- 6-axis or 9-axis IMU mounted to gimbal body
- separate regulated actuator power
- common ground between logic and actuator supply
- emergency unplug or power switch

Key electronics risks:

- servo current causing microcontroller brownout
- IMU vibration/noise
- ground noise coupling into sensor readings
- unstable power from USB-only supply

### Firmware

Purpose: run deterministic control and log test data.

Firmware modules:

- actuator command interface
- IMU read/calibration
- command profile generator
- PID controller
- safety limits
- serial telemetry logger

Telemetry columns:

```text
time_s, cmd_pitch_deg, cmd_yaw_deg,
meas_pitch_deg, meas_yaw_deg,
gyro_x_radps, gyro_y_radps, gyro_z_radps,
err_pitch_deg, err_yaw_deg,
actuator_pitch_us, actuator_yaw_us,
mode
```

### Test And Analysis

Purpose: convert real hardware data into engineering evidence.

Initial plots:

- commanded vs measured pitch
- commanded vs measured yaw
- tracking error vs time
- actuator output vs time
- step response metrics
- disturbance rejection response

## Control Development Sequence

1. Actuator neutral and range calibration.
2. Open-loop command sweep.
3. Single-axis step response.
4. Single-axis PID tracking.
5. Two-axis coupled tracking.
6. Disturbance rejection.
7. Optional model-based controller comparison.

## Physical Interpretation

The test stand is a hardware analog of the simulator TVC loop:

```text
controller command -> actuator dynamics -> achieved gimbal angle -> measured attitude/rate
```

The main engineering question is not whether a servo can move. The question is whether the achieved motion follows the command with enough bandwidth, low enough steady-state error, and small enough backlash/noise to support closed-loop attitude control.
