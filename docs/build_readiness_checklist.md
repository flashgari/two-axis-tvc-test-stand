# Rev A Build Readiness Checklist

## Objective

Prepare the two-axis TVC test stand for fabrication, assembly, and first powered testing without relying on memory or improvisation. This checklist is completed before hardware is purchased, printed, or assembled.

The build is considered ready when the project can move through:

```text
print parts -> inspect parts -> assemble mechanism -> calibrate neutral -> collect first data
```

without needing to invent test criteria during the build.

## Print Preparation

| Item | Status | Notes |
| --- | --- | --- |
| All Rev A STL files exported |  | `cad/exports/rev_a_parts/` |
| Part manifest reviewed |  | `cad/rev_a_part_manifest.md` |
| Print material selected |  | PETG preferred; PLA+ acceptable for fit check |
| Layer height selected |  | baseline `0.20 mm` |
| Wall count selected |  | baseline `4` perimeters |
| Infill selected |  | baseline `35-50%` |
| Servo mount print orientation reviewed |  | avoid weak layer lines across servo reaction loads |
| Hard-stop print orientation reviewed |  | stop faces should not fail by layer delamination |
| Support material requirements reviewed |  | minimize supports near bearing/servo surfaces |
| Spare small parts planned |  | print extra hard stops and strain-relief clips |

Physical interpretation:

- Print orientation changes effective stiffness and failure mode. A servo mount loaded across weak layer adhesion can flex or creep, which lowers the effective plant stiffness `k` and can show up as overshoot, slow settling, or neutral drift.
- Hard stops are impact/load-limit features, so layer direction matters. A hard stop that delaminates during an overtravel event no longer protects the servo or gimbal.
- PETG is preferred for Rev A functional testing because it is less brittle and more creep/temperature tolerant than basic PLA, though PLA+ is fine for dimensional fit checks.

## Tools And Consumables

| Item | Ready? | Notes |
| --- | --- | --- |
| calipers |  | required for dimension verification |
| small screwdrivers / hex keys |  | servo hardware and printed assembly |
| drill bits or reamers |  | only for cleanup, not redesign-by-drill |
| washers/spacers |  | prevent fastener heads from crushing plastic |
| threadlocker or locknuts |  | use carefully near plastic |
| multimeter |  | servo supply verification |
| USB data cable |  | must support data, not only charging |
| camera/phone tripod |  | repeatable portfolio video evidence |
| labels/tape |  | label pitch/yaw servos and harnesses |

Physical interpretation:

- Caliper measurements are not paperwork. They close the loop between CAD assumptions and the real manufactured plant.
- Washers and spacers reduce local plastic crushing, which matters because asymmetric preload can add friction and bias torque to the gimbal.
- Voltage measurement during motion separates actuator torque problems from mechanical binding problems.

## Electronics Readiness

| Item | Status | Notes |
| --- | --- | --- |
| Pico firmware loads successfully |  | neutral mode first |
| Servo supply polarity verified |  | before connecting servo |
| Common ground plan verified |  | Pico GND and servo supply GND connected |
| Servo signal pins documented |  | pitch and yaw unambiguous |
| BNO085 wiring documented |  | I2C pins and voltage level |
| Serial logger command prepared |  | `scripts/serial_logger.py` |
| Data template prepared |  | `data/templates/hardware_step_log_template.csv` |

Physical interpretation:

- A missing common ground makes the PWM signal physically undefined at the servo input even if the code is correct.
- Supply droop reduces usable servo torque and speed. If step response is slow while voltage sags, the plant problem is electrical authority, not only mechanical inertia.
- IMU sign errors create control-law sign errors. A mathematically stable controller can become positive feedback if the measured output sign is reversed.

## Assembly Readiness

| Item | Status | Notes |
| --- | --- | --- |
| Assembly order defined |  | base -> yaw servo -> yaw frame -> pitch axis -> nozzle/IMU |
| Servo horns remain removed for first power |  | required safety gate |
| Hard stops installed before sweep |  | protect mechanism |
| Wire strain relief installed before motion |  | avoid cable torque bias |
| Manual sweep completed before power |  | confirm no binding |
| IMU mounted rigidly |  | avoid vibration-corrupted rate data |
| Base clamped or stabilized |  | prevent base motion contaminating measurement |

Physical interpretation:

- Manual sweep detects geometric binding before the servo injects torque into the mechanism.
- Wire strain relief matters dynamically because harness stiffness behaves like an unmodeled torsional spring.
- Base motion contaminates measured gimbal response. If the base moves, the IMU measurement is no longer the isolated plant output.

## Data Readiness

| Item | Status | Notes |
| --- | --- | --- |
| Calibration worksheet prepared |  | `docs/hardware_calibration_worksheet.md` |
| First-test report template prepared |  | `docs/first_test_report_template.md` |
| Raw data naming convention selected |  | `YYYYMMDD_axis_testid.csv` |
| Prediction metrics available |  | `data/examples/prehardware_*metrics.json` |
| Plot scripts verified |  | `scripts/plot_step_response.py` |
| Analysis scripts verified |  | `scripts/analyze_step_response.py` |

Recommended raw data names:

```text
data/20260721_pitch_step_2deg_a.csv
data/20260721_pitch_step_5deg_a.csv
data/20260721_yaw_step_2deg_a.csv
data/20260721_yaw_step_5deg_a.csv
data/20260721_pitch_hysteresis_5deg_a.csv
data/20260721_yaw_hysteresis_5deg_a.csv
```

Physical interpretation:

- Consistent filenames preserve the link between test condition, axis, raw data, metrics, and plots.
- The pre-hardware prediction is the baseline. The first measured response should be interpreted as an update to `I_axis`, `c`, `k`, disturbance torque, actuator lag, or actuator torque authority.

## Build Readiness Gate

Do not begin powered gimbal testing until:

- servo horns have been removed for first neutral power-on
- servo supply polarity and voltage have been verified
- common ground has been verified
- mechanical hard stops are installed
- manual sweep shows no binding through the firmware command range
- the first raw log filename and report template are prepared

This gate prevents the first hardware session from becoming an uncontrolled troubleshooting session.
