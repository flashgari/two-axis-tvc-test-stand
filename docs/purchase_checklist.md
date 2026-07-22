# Purchase Checklist

## Prototype 1 Baseline

This checklist is based on the selected low-cost Option A architecture.

Exact vendor candidates are tracked in [vendor_shortlist.md](vendor_shortlist.md). Check current price and availability again immediately before ordering.

## Electronics

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| Raspberry Pi Pico H or equivalent RP2040 board with headers | 1 | Candidate selected | Pre-soldered headers recommended for speed |
| Adafruit BNO085-class IMU breakout | 1 | Candidate selected | STEMMA/Qwiic connector useful |
| Hitec HS-625MG metal-gear PWM servos | 2 | Selected | Traceable torque, speed, mass, spline, and dimensions for CAD/test documentation |
| External `5 V`, `4 A` servo supply | 1 | Candidate selected | Must handle stall/current spikes |
| `2.1 mm` barrel jack to screw-terminal adapter | 1 | Candidate selected | Clean servo-power distribution |
| Breadboard or protoboard | 1 | TBD | For first wiring pass |
| Jumper wires | 1 set | TBD | Include male/female options |
| STEMMA QT/Qwiic I2C cable | 1 | Candidate selected | Match IMU connector |
| USB cable | 1 | TBD | Data-capable cable |

## Mechanical

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| PLA+/PETG filament | 1 spool or available stock | TBD | PETG preferred if available |
| M3 screw assortment | 1 set | TBD | Common for printed mechanisms |
| M3 heat-set inserts | optional | TBD | Improves serviceability |
| Small bearings/shafts | TBD | TBD | Depends on CAD layout |
| Servo horns/linkages | TBD | TBD | Often included with servos |
| Rubber feet/clamps | TBD | TBD | Stabilize base on bench |

## Tools

| Tool | Needed? | Notes |
| --- | --- | --- |
| 3D printer access | yes | For first gimbal parts |
| Soldering iron | likely | Headers/connectors |
| Multimeter | yes | Power and continuity checks |
| Calipers | yes | CAD and assembly verification |
| Small screwdrivers/hex keys | yes | Assembly |
| Protractor/angle reference | useful | Independent angle check |

## Before Buying

- [x] Choose Servo Path A from `docs/vendor_shortlist.md`.
- [ ] Confirm HS-625MG dimensions, spline, horn package, wire length, and stall-current estimate.
- [ ] Confirm IMU breakout voltage and connector type.
- [ ] Confirm Pico header option.
- [ ] Confirm servo supply voltage/current rating.
- [ ] Confirm CAD envelope so servos physically fit.
- [ ] Check whether bearings/shafts are needed or if servo output shafts carry Prototype 1.

## Budget Target

Prototype 1 target budget:

```text
about $165-220 before tools, tax, and shipping
```

If the total exceeds this range, reduce scope before buying more expensive electronics. The goal is first hardware data, not final flight-like hardware.

The selected path is the Pico/BNO085 electronics stack plus two traceable Hitec HS-625MG servos. This is more expensive than the strict-budget servo pack, but it gives the project stronger CAD inputs and a cleaner actuator-specification trail.
