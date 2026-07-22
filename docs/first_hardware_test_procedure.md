# First Hardware Test Procedure

## Objective

Safely run the first Pico/servo/telemetry test without damaging the Rev A gimbal or corrupting the data. This procedure starts with the horn removed, verifies neutral PWM, then progresses to limited motion.

## Required Hardware

- Raspberry Pi Pico H
- one HS-625MG servo
- external `5 V`, `4 A` servo supply
- `2.1 mm` barrel jack to screw terminal adapter
- jumper wires
- data-capable USB cable
- multimeter
- printed yaw servo mount or loose bench setup
- laptop with repo scripts

Do **not** install the servo horn for the first powered neutral test.

## Safety Logic

The firmware limit is:

```text
+/-10 deg
```

The mechanical hard-stop target is:

```text
about +/-15 deg
```

This margin exists because:

```text
unknown servo zero + installed horn + powered command = possible hard-stop impact
```

The first powered test must therefore verify neutral before the horn is attached.

## Electrical Setup

```text
laptop USB -> Pico
Pico PWM pin -> servo signal
external 5 V supply + -> servo red wire
external 5 V supply GND -> servo brown/black wire
Pico GND -> servo supply GND
```

The common ground is required because the PWM signal is measured relative to the servo ground. Without common ground, the servo input does not have a valid voltage reference.

## Step 1: Pico-Only Serial Test

1. Copy `firmware/src/*.py` onto the Pico.
2. Confirm `MODE = "neutral"` in `firmware/src/main.py`.
3. Plug Pico into USB.
4. Open serial monitor or use the logger once the port is known.

Expected telemetry:

```text
pitch_cmd_deg = 0
yaw_cmd_deg = 0
pitch_pwm_us = 1500
yaw_pwm_us = 1500
```

Pass condition:

- CSV header appears
- rows stream at about `50 Hz`
- no servo connected yet

## Step 2: Power Verification

1. Plug in the `5 V`, `4 A` supply.
2. Measure screw-terminal voltage with multimeter.
3. Confirm polarity before connecting servo.

Pass condition:

```text
servo supply ~= 5 V
polarity correct
```

## Step 3: Servo Neutral With Horn Removed

1. Connect servo power and ground.
2. Connect servo signal to the configured Pico PWM pin.
3. Ensure servo horn is removed.
4. Power Pico and servo.

Expected behavior:

- servo moves to neutral internally
- no mechanism is attached
- no brownout or USB disconnect occurs

Physical interpretation:

If the Pico resets when the servo moves, the servo supply wiring or ground reference is likely wrong. If the servo jitters, check common ground and supply stiffness before blaming the firmware.

## Step 4: Horn Installation

1. Power off servo supply.
2. Install horn as close to mechanical neutral as possible.
3. Keep the mechanism disconnected or free to move.
4. Power on in `neutral` mode again.

Pass condition:

- horn returns to expected neutral
- no hard-stop contact
- no visible servo chatter

## Step 5: Limited Sweep

Only after neutral is confirmed:

1. Change `MODE` to `sweep_pitch` or `sweep_yaw`.
2. Keep the first sweep unloaded or lightly loaded.
3. Watch for binding through the command range.
4. Log serial data:

```bash
python3 scripts/serial_logger.py --port /dev/tty.usbmodemXXXX
```

## Step 6: Analyze The First Log

```bash
python3 scripts/analyze_step_response.py data/<log>.csv --axis pitch
python3 scripts/plot_step_response.py data/<log>.csv --axis pitch
```

The first log may not include measured angle until the BNO085 driver is active. In that case, the important first result is correct command timing, PWM limits, and no power/reset faults.

## What Each Failure Means Physically

| Observation | Likely cause | Engineering response |
| --- | --- | --- |
| Pico resets when servo moves | servo current sag or missing common ground | verify external supply and ground wiring |
| servo jitters at neutral | noisy power, invalid signal reference, or deadband chatter | shorten wiring, check ground, log supply behavior |
| horn hits stop at neutral | horn installed at wrong spline index | power off, reinstall horn closer to neutral |
| motion binds near limit | CAD/mount alignment or hard-stop placement issue | adjust slotted mount or Rev A geometry |
| measured angle biased at rest | CM offset, wire preload, or horn offset | rebalance/reroute wires/calibrate neutral |
| response differs by approach direction | backlash, horn slop, friction | quantify hysteresis before PID tuning |

## Required Test Record

For the portfolio, save:

- date
- hardware revision
- firmware commit
- wiring photo
- setup photo
- raw CSV log
- generated plot
- metrics JSON
- observations and failure notes

The goal is not a perfect first test. The goal is a traceable design-build-test loop.
