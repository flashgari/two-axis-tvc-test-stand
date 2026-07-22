"""CSV telemetry helpers."""

FIELDS = [
    "time_ms",
    "mode",
    "pitch_cmd_deg",
    "yaw_cmd_deg",
    "pitch_pwm_us",
    "yaw_pwm_us",
    "imu_present",
    "quat_w",
    "quat_x",
    "quat_y",
    "quat_z",
    "gyro_x_dps",
    "gyro_y_dps",
    "gyro_z_dps",
]


def print_header():
    print(",".join(FIELDS))


def print_row(values):
    row = []
    for field in FIELDS:
        value = values.get(field, "")
        if isinstance(value, float):
            row.append("{:.6f}".format(value))
        else:
            row.append(str(value))
    print(",".join(row))
