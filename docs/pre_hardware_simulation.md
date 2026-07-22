# Pre-Hardware Gimbal Simulation

## Objective

Create a prediction baseline before hardware arrives. The goal is not to claim the model is exact. The goal is to state the assumptions clearly, predict first-order behavior, then compare the prediction against measured data after the first servo tests.

## Model

Each gimbal axis is modeled as:

```text
I_axis theta_ddot + c theta_dot + k theta = tau_servo + tau_disturbance
```

The servo is modeled as a first-order actuator lag:

```text
delta_dot = (delta_cmd - delta) / tau_servo_lag
```

and the torque command is saturated:

```text
tau_servo = clamp(K_servo (delta - theta), -tau_limit, +tau_limit)
```

This captures the key physical effects expected in Rev A:

- moving inertia from the printed gimbal/nozzle
- damping from bearings, geartrain friction, and structural losses
- stiffness from gravity coupling, printed-frame compliance, and wire preload
- actuator lag from the HS-625MG internal servo loop
- saturation from finite useful torque
- disturbance torque from center-of-mass offset and cable loads

## Assumptions

The simulation uses the current Rev A mass/inertia estimates:

| Axis | Inertia | Gravity/disturbance torque | Interpretation |
| --- | ---: | ---: | --- |
| pitch | `3.0e-5 kg m^2` | `0.018 N m` | lighter moving carrier and nozzle |
| yaw | `3.0e-4 kg m^2` | `0.039 N m` | larger inertia because yaw carries the pitch subsystem |

The useful servo torque is capped at `0.13 N m`, about `20%` of the HS-625MG stall torque at `6 V`. This avoids pretending stall torque is available for clean dynamic control.

## Generated Files

Run:

```bash
python3 scripts/simulate_pre_hardware_response.py
python3 scripts/analyze_step_response.py data/examples/prehardware_pitch_step_prediction.csv --axis pitch
python3 scripts/analyze_step_response.py data/examples/prehardware_yaw_step_prediction.csv --axis yaw
python3 scripts/plot_step_response.py data/examples/prehardware_pitch_step_prediction.csv --axis pitch
python3 scripts/plot_step_response.py data/examples/prehardware_yaw_step_prediction.csv --axis yaw
```

Outputs:

```text
data/examples/prehardware_model_parameters.json
data/examples/prehardware_pitch_step_prediction.csv
data/examples/prehardware_yaw_step_prediction.csv
data/examples/prehardware_pitch_step_prediction.pitch.metrics.json
data/examples/prehardware_yaw_step_prediction.yaw.metrics.json
plots/examples/prehardware_pitch_step_prediction_pitch_step_response.svg
plots/examples/prehardware_yaw_step_prediction_yaw_step_response.svg
```

## Upper-Division Physical Interpretation

The pre-hardware model is valuable because it creates a falsifiable expectation:

- If measured rise time is much slower than predicted, actuator lag, friction, or binding is larger than assumed.
- If measured steady-state error is larger than predicted, center-of-mass offset, wire preload, or servo deadband is likely under-modeled.
- If measured overshoot is larger than predicted, damping is lower or structural compliance is higher than assumed.
- If measured response depends on approach direction, backlash/hysteresis is missing from the current linear model.
- If yaw performs much worse than pitch, the larger yaw inertia and pitch-servo-on-yaw mass are probably dominating.

This makes the first hardware data more meaningful. The plot is not just "what happened"; it becomes a comparison between predicted plant behavior and measured plant behavior.

## How This Supports The Portfolio

This is the correct engineering sequence:

```text
CAD mass estimate -> pre-hardware dynamic model -> predicted plots -> physical test -> model update
```

That sequence shows aerospace reasoning because it connects geometry, mass properties, actuator limits, differential equations, measured response, and design iteration.
