# Data Templates

These CSV templates define the expected structure for first hardware logs.

| File | Purpose |
| --- | --- |
| `calibration_record_template.csv` | Records neutral PWM, mechanical zero, range, voltage, IMU bias, and hysteresis observations. |
| `hardware_step_log_template.csv` | Defines the telemetry columns required by the step-response analysis pipeline. |

The most important fields for analysis are:

```text
time_ms
pitch_cmd_deg / yaw_cmd_deg
meas_pitch_deg / meas_yaw_deg
pitch_pwm_us / yaw_pwm_us
gyro_pitch_dps / gyro_yaw_dps
```

The extra fields, such as `servo_supply_v`, `imu_status`, `test_id`, and `notes`, make the data useful for engineering diagnosis. For example, a slow response with a simultaneous supply-voltage drop points to actuator power margin, while a clean voltage trace with high hysteresis points more toward backlash, friction, or spline looseness.

The first measured log should be analyzed with:

```bash
python3 scripts/analyze_step_response.py data/<log>.csv --axis pitch
python3 scripts/plot_step_response.py data/<log>.csv --axis pitch
```

Then compare the result against the pre-hardware prediction files in `data/examples/`.
