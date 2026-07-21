# Data

Raw test logs will live here.

Expected CSV format:

```text
time_s, cmd_pitch_deg, cmd_yaw_deg,
meas_pitch_deg, meas_yaw_deg,
gyro_x_radps, gyro_y_radps, gyro_z_radps,
err_pitch_deg, err_yaw_deg,
actuator_pitch_us, actuator_yaw_us,
mode
```

Keep raw logs unchanged. Processed plots should go in `plots/`.
