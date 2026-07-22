# Tests

Hardware test procedures and analysis scripts will live here.

Test categories:

- mechanical range tests
- actuator calibration tests
- IMU calibration tests
- open-loop step-response tests
- closed-loop tracking tests
- disturbance rejection tests

Host-side software tests can be run with:

```bash
python3 -m unittest discover firmware/tests
python3 -m unittest discover tests
```
