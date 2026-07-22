import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

from actuators import angle_to_pwm_us, clamp_angle_deg, pwm_us_to_duty_u16
from config import (
    FIRMWARE_LIMIT_DEG,
    SERVO_MAX_US,
    SERVO_MIN_US,
    SERVO_NEUTRAL_US,
    US_PER_DEG,
)


class ActuatorMappingTests(unittest.TestCase):
    def test_angle_clamp_limits_commands(self):
        self.assertEqual(clamp_angle_deg(99.0), FIRMWARE_LIMIT_DEG)
        self.assertEqual(clamp_angle_deg(-99.0), -FIRMWARE_LIMIT_DEG)
        self.assertEqual(clamp_angle_deg(3.5), 3.5)

    def test_neutral_maps_to_neutral_pwm(self):
        self.assertEqual(angle_to_pwm_us(0.0), SERVO_NEUTRAL_US)

    def test_positive_and_negative_angles_map_symmetrically(self):
        self.assertEqual(angle_to_pwm_us(5.0), SERVO_NEUTRAL_US + int(5 * US_PER_DEG))
        self.assertEqual(angle_to_pwm_us(-5.0), SERVO_NEUTRAL_US - int(5 * US_PER_DEG))

    def test_pwm_mapping_never_exceeds_servo_bounds(self):
        self.assertLessEqual(SERVO_MIN_US, angle_to_pwm_us(999.0))
        self.assertGreaterEqual(SERVO_MAX_US, angle_to_pwm_us(999.0))
        self.assertLessEqual(SERVO_MIN_US, angle_to_pwm_us(-999.0))
        self.assertGreaterEqual(SERVO_MAX_US, angle_to_pwm_us(-999.0))

    def test_pwm_to_duty_is_in_u16_range(self):
        for pwm_us in (SERVO_MIN_US, SERVO_NEUTRAL_US, SERVO_MAX_US):
            duty = pwm_us_to_duty_u16(pwm_us)
            self.assertLessEqual(0, duty)
            self.assertGreaterEqual(65535, duty)


if __name__ == "__main__":
    unittest.main()
