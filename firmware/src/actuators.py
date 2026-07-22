"""Servo actuator mapping for the two-axis TVC stand.

The servo command is not treated as an ideal angle source. The output is a
bounded PWM request that will later be compared against measured IMU response.
"""

try:
    from machine import Pin, PWM
except ImportError:  # Allows host-side unit tests without MicroPython.
    Pin = None
    PWM = None

from config import (
    FIRMWARE_LIMIT_DEG,
    SERVO_MAX_US,
    SERVO_MIN_US,
    SERVO_NEUTRAL_US,
    SERVO_PWM_HZ,
    US_PER_DEG,
)


def clamp(value, low, high):
    return max(low, min(high, value))


def clamp_angle_deg(angle_deg):
    return clamp(float(angle_deg), -FIRMWARE_LIMIT_DEG, FIRMWARE_LIMIT_DEG)


def angle_to_pwm_us(angle_deg):
    """Map desired nozzle angle to PWM microseconds with safety clamping."""
    limited_angle = clamp_angle_deg(angle_deg)
    pwm_us = SERVO_NEUTRAL_US + US_PER_DEG * limited_angle
    return int(round(clamp(pwm_us, SERVO_MIN_US, SERVO_MAX_US)))


def pwm_us_to_duty_u16(pwm_us, pwm_hz=SERVO_PWM_HZ):
    """Convert pulse width to Pico PWM duty_u16 units."""
    period_us = 1_000_000.0 / pwm_hz
    duty_fraction = clamp(pwm_us / period_us, 0.0, 1.0)
    return int(round(duty_fraction * 65535))


class ServoAxis:
    def __init__(self, pin_id, name):
        self.name = name
        self.last_cmd_deg = 0.0
        self.last_pwm_us = SERVO_NEUTRAL_US
        self._pwm = None

        if PWM is not None:
            self._pwm = PWM(Pin(pin_id))
            self._pwm.freq(SERVO_PWM_HZ)

    def command_deg(self, angle_deg):
        self.last_cmd_deg = clamp_angle_deg(angle_deg)
        self.last_pwm_us = angle_to_pwm_us(self.last_cmd_deg)

        if self._pwm is not None:
            self._pwm.duty_u16(pwm_us_to_duty_u16(self.last_pwm_us))

        return self.last_cmd_deg, self.last_pwm_us

    def neutral(self):
        return self.command_deg(0.0)
