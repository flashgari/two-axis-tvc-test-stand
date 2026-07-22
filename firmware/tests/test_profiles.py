import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

from config import STEP_AMPLITUDE_DEG, SWEEP_AMPLITUDE_DEG
from profiles import neutral_profile, step_pitch_profile, sweep_pitch_profile, sweep_yaw_profile


class ProfileTests(unittest.TestCase):
    def test_neutral_profile_commands_zero(self):
        self.assertEqual(neutral_profile(1.23), (0.0, 0.0))

    def test_sweep_profiles_stay_inside_command_amplitude(self):
        for t_s in (0.0, 0.5, 1.0, 2.0, 3.0):
            pitch, yaw = sweep_pitch_profile(t_s)
            self.assertLessEqual(abs(pitch), SWEEP_AMPLITUDE_DEG)
            self.assertEqual(yaw, 0.0)

            pitch, yaw = sweep_yaw_profile(t_s)
            self.assertEqual(pitch, 0.0)
            self.assertLessEqual(abs(yaw), SWEEP_AMPLITUDE_DEG)

    def test_step_profile_alternates_pitch_command(self):
        pitch_0, yaw_0 = step_pitch_profile(0.1)
        pitch_1, yaw_1 = step_pitch_profile(2.1)
        self.assertEqual(pitch_0, STEP_AMPLITUDE_DEG)
        self.assertEqual(pitch_1, -STEP_AMPLITUDE_DEG)
        self.assertEqual(yaw_0, 0.0)
        self.assertEqual(yaw_1, 0.0)


if __name__ == "__main__":
    unittest.main()
