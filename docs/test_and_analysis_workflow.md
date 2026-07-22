# Test And Analysis Workflow

## Objective

Create a repeatable verification path from Pico telemetry to engineering plots and metrics.

```text
Pico USB serial CSV -> saved log -> analysis metrics -> plots -> physical interpretation
```

This matters because the project claim is not simply that the test stand moves. The claim is that the hardware can be designed, built, measured, and improved using evidence.

## Current Scripts

| Script | Purpose |
| --- | --- |
| `scripts/serial_logger.py` | Capture Pico USB serial CSV into `data/`. |
| `scripts/generate_synthetic_step_log.py` | Generate a synthetic step-response log before hardware is available. |
| `scripts/analyze_step_response.py` | Compute step-response metrics from a CSV log. |
| `scripts/plot_step_response.py` | Generate command/response/error/PWM plots. |
| `scripts/tvc_analysis.py` | Shared analysis functions used by scripts and tests. |

## Synthetic Pipeline

Run from the repo root:

```bash
python3 scripts/generate_synthetic_step_log.py
python3 scripts/analyze_step_response.py data/examples/synthetic_pitch_step.csv --axis pitch
python3 scripts/plot_step_response.py data/examples/synthetic_pitch_step.csv --axis pitch
```

Outputs:

```text
data/examples/synthetic_pitch_step.csv
data/examples/synthetic_pitch_step.pitch.metrics.json
plots/examples/synthetic_pitch_step_pitch_step_response.svg
```

## Hardware Pipeline

After the Pico is connected:

```bash
python3 scripts/serial_logger.py --port /dev/tty.usbmodemXXXX
```

Then run:

```bash
python3 scripts/analyze_step_response.py data/<log>.csv --axis pitch
python3 scripts/plot_step_response.py data/<log>.csv --axis pitch
```

## Upper-Division Physical Interpretation

The measured response should be interpreted through the rotational plant:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The metrics are not generic plotting quantities. Each one maps to a physical mechanism:

| Metric | Physical interpretation |
| --- | --- |
| response delay | actuator electronics, servo internal loop delay, IMU/filter delay, or command transport latency |
| rise time | combined servo speed, moving inertia, and effective control authority |
| overshoot | low damping, frame compliance, servo internal control behavior, or excessive command aggressiveness |
| settling time | damping, structural flex, bearing friction, and sensor filtering |
| steady-state error | center-of-mass gravity bias, wire preload, servo deadband, or horn offset |
| peak tracking error | worst transient pointing error during maneuver |
| hysteresis bias | gear backlash, horn slop, friction, or approach-direction dependence |

For a TVC mechanism, static torque margin alone is insufficient. A servo can hold the nozzle and still be a poor actuator if it has excessive phase lag, deadband, backlash, or voltage-sensitive response. The analysis pipeline exists to expose those effects quantitatively.

## What Makes A Good First Result

For Rev A, a good result is not perfect tracking. A good result is a clean dataset that identifies the dominant nonideality:

- if the response is slow, actuator bandwidth is the likely limiter
- if the final angle is biased, check CM offset and wire preload
- if the path depends on approach direction, backlash/hysteresis is likely
- if the response rings or rebounds, check structural compliance and damping
- if telemetry jumps during motion, check IMU mounting and power noise

That evidence drives Rev B CAD and firmware changes.
