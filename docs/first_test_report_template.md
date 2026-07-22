# First Hardware Test Report Template

## Test Metadata

| Field | Entry |
| --- | --- |
| Test date |  |
| Hardware revision | Rev A |
| Firmware commit |  |
| CAD commit |  |
| Operator |  |
| Test location |  |
| Servo supply voltage |  |
| Printed material/settings |  |
| Data files |  |
| Plot files |  |

## Test Objective

State the purpose of this test campaign.

Example:

```text
Measure the first open-loop pitch/yaw step response of the Rev A two-axis TVC
test stand and compare the measured plant behavior against the pre-hardware
dynamic prediction.
```

## Setup Evidence

Add photo/video links or filenames.

| Evidence | File / link | What it proves |
| --- | --- | --- |
| assembled test stand photo |  | mechanism physically built |
| wiring photo |  | servo power and common ground are traceable |
| servo-neutral video |  | safe bring-up with horn removed |
| pitch step video |  | pitch axis moves under command |
| yaw step video |  | yaw axis moves under command |
| plot screenshot |  | motion is measured, not only observed |

## Configuration Summary

| Item | Value / note |
| --- | --- |
| Pitch neutral PWM |  |
| Yaw neutral PWM |  |
| Pitch mechanical zero offset |  |
| Yaw mechanical zero offset |  |
| Pitch hard-stop angle |  |
| Yaw hard-stop angle |  |
| IMU axis convention verified | yes / no |
| Wire strain relief installed | yes / no |
| Base clamped or stabilized | yes / no |

Physical interpretation:

- Neutral offsets are trim biases. If they are large, the servo uses part of its authority cancelling a DC moment before tracking dynamic commands.
- Hard-stop angles define the nonlinear safety boundary. Repeated hard-stop contact invalidates a simple linear step-response interpretation.
- IMU axis verification prevents a sign error from being misdiagnosed as controller instability.

## Test Matrix

| Test ID | Axis | Command | Raw CSV | Metrics JSON | Plot | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `PITCH_STEP_2DEG_A` | pitch | `0 -> +2 deg -> 0` |  |  |  |  |
| `PITCH_STEP_5DEG_A` | pitch | `0 -> +5 deg -> 0` |  |  |  |  |
| `YAW_STEP_2DEG_A` | yaw | `0 -> +2 deg -> 0` |  |  |  |  |
| `YAW_STEP_5DEG_A` | yaw | `0 -> +5 deg -> 0` |  |  |  |  |
| `PITCH_HYST_5DEG_A` | pitch | `-5 -> +5 -> -5 deg` |  |  |  |  |
| `YAW_HYST_5DEG_A` | yaw | `-5 -> +5 -> -5 deg` |  |  |  |  |

## Analysis Commands

Pitch example:

```bash
python3 scripts/analyze_step_response.py data/<pitch_log>.csv --axis pitch
python3 scripts/plot_step_response.py data/<pitch_log>.csv --axis pitch
```

Yaw example:

```bash
python3 scripts/analyze_step_response.py data/<yaw_log>.csv --axis yaw
python3 scripts/plot_step_response.py data/<yaw_log>.csv --axis yaw
```

## Results Summary

| Metric | Pitch prediction | Pitch measured | Yaw prediction | Yaw measured | Interpretation |
| --- | ---: | ---: | ---: | ---: | --- |
| response delay |  |  |  |  | actuator lag / deadband / filtering |
| rise time |  |  |  |  | torque-to-inertia ratio |
| overshoot |  |  |  |  | damping and compliance |
| settling time |  |  |  |  | damping, stiffness, lag |
| steady-state error |  |  |  |  | bias torque / deadband / calibration |
| peak tracking error |  |  |  |  | maximum pointing transient |
| hysteresis bias |  |  |  |  | backlash / friction / horn slop |

## Plot Interpretation

### Pitch Step Response

Insert pitch plot:

```text
plots/<pitch_plot>.svg
```

Upper-division physical interpretation:

- If measured pitch rise time is close to prediction, the pitch-axis inertia and useful torque assumptions are reasonable.
- If measured pitch rise time is slower, the likely missing terms are servo lag, friction, binding, underestimated inertia, or supply-voltage sag.
- If overshoot is higher than prediction, Rev A pitch damping is lower than modeled or frame/servo compliance is adding phase lag.
- If steady-state error remains after the step settles, the pitch axis has trim bias from center-of-mass offset, wire preload, horn indexing, or servo deadband.

### Yaw Step Response

Insert yaw plot:

```text
plots/<yaw_plot>.svg
```

Upper-division physical interpretation:

- Yaw should generally be slower than pitch because the yaw axis carries the full pitch subsystem.
- If yaw is much worse than prediction, inspect yaw-frame stiffness, yaw servo mount preload, and mass placement relative to the yaw axis.
- If yaw response differs depending on approach direction, the dominant issue is likely backlash or Coulomb friction rather than only inertia.
- If yaw shows ringing, the outer frame may be behaving as a compliant structure rather than a rigid body.

## Failure / Anomaly Log

| Observation | Time / test ID | Likely physical cause | Immediate action | Rev B implication |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

Common interpretations:

- Pico reset during motion: servo current transient, supply sag, or grounding issue.
- Servo jitter at neutral: signal reference, supply noise, servo deadband, or mechanical preload.
- Nozzle sticks then jumps: static friction or backlash.
- Response changes across repeats: looseness, heating, wire motion, or inconsistent preload.
- IMU angle jumps during motion: sensor mounting vibration, I2C issue, or filtering artifact.

## Prediction Versus Measurement

State whether the pre-hardware model captured the main behavior.

```text
The model did / did not predict the dominant response trend because...
```

Tie the comparison to the plant equation:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

Interpretation prompts:

- Was the inertia estimate reasonable?
- Was damping higher or lower than expected?
- Did the structure behave as rigid, or was compliance visible?
- Was there an unmodeled constant disturbance torque?
- Did actuator lag dominate the response?
- Did saturation appear during larger commands?
- Did backlash/hysteresis violate the linear model?

## Rev B Action Items

| Priority | Action | Physical reason | Evidence |
| --- | --- | --- | --- |
| high |  |  |  |
| medium |  |  |  |
| low |  |  |  |

Example actions:

- reduce yaw inertia by moving mass closer to the yaw axis
- stiffen the outer yaw frame if yaw rings or settles slowly
- improve horn coupling if hysteresis bias is large
- reroute wires if steady-state bias changes with harness position
- improve supply wiring if voltage droop correlates with slow response
- tune controller only after mechanical friction/backlash are understood

## Conclusion

Summarize the test in engineering terms:

```text
Rev A successfully demonstrated / did not yet demonstrate controlled two-axis
motion. The dominant measured limitation was ____. The next iteration should
address ____ because the data show ____.
```

The final report should make the design-build-test loop explicit:

```text
CAD assumption -> pre-hardware prediction -> measured data -> physical cause -> Rev B decision
```
