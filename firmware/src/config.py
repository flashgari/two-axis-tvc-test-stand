"""Prototype 1 firmware configuration.

Units are explicit because firmware constants become physical assumptions.
The first hardware tests should update these values after calibration.
"""

# Control-loop timing.
LOOP_HZ = 50
LOOP_DT_S = 1.0 / LOOP_HZ

# Raspberry Pi Pico GPIO assignments.
PITCH_SERVO_PIN = 14
YAW_SERVO_PIN = 15
I2C_SDA_PIN = 4
I2C_SCL_PIN = 5
I2C_FREQ_HZ = 400_000

# Servo PWM convention for hobby servos.
SERVO_PWM_HZ = 50
SERVO_MIN_US = 1000
SERVO_NEUTRAL_US = 1500
SERVO_MAX_US = 2000

# Commanded gimbal envelope.
FIRMWARE_LIMIT_DEG = 10.0
MECHANICAL_STOP_DEG = 15.0

# Initial angle-to-PWM slope.
# This is deliberately conservative: +/-10 deg maps to +/-200 us.
# Update after measuring actual horn/gimbal geometry.
US_PER_DEG = 20.0

# Test profile settings.
SWEEP_AMPLITUDE_DEG = 8.0
SWEEP_PERIOD_S = 4.0
STEP_AMPLITUDE_DEG = 5.0
STEP_PERIOD_S = 2.0

# BNO085 I2C address is commonly 0x4A or 0x4B depending on breakout setup.
BNO085_I2C_ADDR_CANDIDATES = (0x4A, 0x4B)
