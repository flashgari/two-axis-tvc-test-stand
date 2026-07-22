# Data

Raw test logs will live here.

Primary hardware step-response CSV format:

```text
time_ms, mode,
pitch_cmd_deg, meas_pitch_deg, pitch_pwm_us, gyro_pitch_dps,
yaw_cmd_deg, meas_yaw_deg, yaw_pwm_us, gyro_yaw_dps,
servo_supply_v, imu_status, test_id, notes
```

Keep raw logs unchanged. Processed metrics remain next to example datasets or next to the raw log, and generated plots should go in `plots/`.

Templates for first hardware testing live in `data/templates/`.

## Examples

Tracked example logs live in `data/examples/`. These are not hardware data; they are synthetic logs used to verify the analysis pipeline before the Pico is connected.

Raw hardware logs in `data/*.csv` are ignored by Git by default so accidental large or messy test files do not enter the repo.

## Physical Interpretation

The CSV format deliberately logs command, measured angle, PWM, gyro rate, and supply voltage together. Those channels separate physical failure modes:

- command changes without measured motion point to deadband, binding, wiring, or actuator power issues
- measured motion with supply-voltage sag points to current draw and power margin
- large gyro spikes with small angle motion point to IMU mounting vibration or sensor/filter artifacts
- final measured angle offset after a step points to gravity bias, wire preload, horn indexing, or servo deadband
- repeated tests with different final angles point to backlash or Coulomb friction rather than a purely linear plant
