import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from tvc_analysis import analyze_step_response, load_csv


class TvcAnalysisTests(unittest.TestCase):
    def test_analyze_step_response_detects_basic_metrics(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "step.csv"
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["time_ms", "pitch_cmd_deg", "meas_pitch_deg", "pitch_pwm_us"],
                )
                writer.writeheader()
                for i in range(101):
                    t = i / 50.0
                    cmd = 0.0 if t < 0.5 else 5.0
                    meas = 0.0 if t < 0.5 else 5.0 * (1.0 - 2.71828 ** (-(t - 0.5) / 0.18))
                    writer.writerow({
                        "time_ms": int(t * 1000),
                        "pitch_cmd_deg": cmd,
                        "meas_pitch_deg": meas,
                        "pitch_pwm_us": int(1500 + 20 * cmd),
                    })

            rows = load_csv(path)
            metrics = analyze_step_response(rows, axis="pitch")
            self.assertEqual(metrics.axis, "pitch")
            self.assertGreater(metrics.step_amplitude_deg, 4.0)
            self.assertIsNotNone(metrics.rise_time_10_90_s)
            self.assertGreater(metrics.peak_abs_error_deg, 0.0)


if __name__ == "__main__":
    unittest.main()
