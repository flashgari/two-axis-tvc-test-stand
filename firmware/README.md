# Firmware

Embedded firmware will live here.

Planned modules:

```text
src/
  main controller loop
  actuator command mapping
  IMU driver/calibration
  PID controller
  safety limits
  serial telemetry
```

Initial firmware milestones:

1. Blink/serial bring-up.
2. Servo neutral command.
3. Servo sweep with angle limits.
4. IMU readout.
5. CSV telemetry stream.
6. Open-loop step profiles.
7. Closed-loop PID.
