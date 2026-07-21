# Purchase Checklist

## Prototype 1 Baseline

This checklist is based on the selected low-cost Option A architecture.

## Electronics

| Item | Qty | Status | Notes |
| --- | ---: | --- | --- |
| Raspberry Pi Pico-class board | 1 | TBD | Pre-soldered headers recommended for speed |
| BNO085-class IMU breakout | 1 | TBD | STEMMA/Qwiic connector useful |
| Metal-gear PWM servos | 2 + optional spare | TBD | Prefer `>= 5 kg-cm` torque |
| External `5-6 V` servo supply | 1 | TBD | Must handle stall/current spikes |
| Breadboard or protoboard | 1 | TBD | For first wiring pass |
| Jumper wires | 1 set | TBD | Include male/female options |
| I2C cable | 1 | TBD | Match IMU connector |
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

- [ ] Confirm final servo torque and dimensions.
- [ ] Confirm IMU breakout voltage and connector type.
- [ ] Confirm Pico header option.
- [ ] Confirm servo supply voltage/current rating.
- [ ] Confirm CAD envelope so servos physically fit.
- [ ] Check whether bearings/shafts are needed or if servo output shafts carry Prototype 1.

## Budget Target

Prototype 1 target budget:

```text
about $85-150 before tools
```

If the total exceeds this range, reduce scope before buying more expensive electronics. The goal is first hardware data, not final flight-like hardware.
