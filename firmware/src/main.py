"""Raspberry Pi Pico Rev A bring-up firmware.

Default mode is neutral for safety. Change MODE only after confirming external
servo power, common ground, and unobstructed mechanical travel.
"""

import time

from actuators import ServoAxis
from config import LOOP_DT_S, LOOP_HZ, PITCH_SERVO_PIN, YAW_SERVO_PIN
from imu_bno085 import BNO085
from profiles import PROFILES
from telemetry import print_header, print_row

# Safe default. Valid modes: neutral, sweep_pitch, sweep_yaw, step_pitch, step_yaw.
MODE = "neutral"


def millis():
    try:
        return time.ticks_ms()
    except AttributeError:
        return int(time.time() * 1000)


def sleep_dt():
    time.sleep(LOOP_DT_S)


def run():
    pitch = ServoAxis(PITCH_SERVO_PIN, "pitch")
    yaw = ServoAxis(YAW_SERVO_PIN, "yaw")
    imu = BNO085()

    profile = PROFILES.get(MODE, PROFILES["neutral"])
    start_ms = millis()

    pitch.neutral()
    yaw.neutral()

    print("# two_axis_tvc_test_stand Rev A firmware")
    print("# loop_hz={}".format(LOOP_HZ))
    print("# mode={}".format(MODE))
    print_header()

    while True:
        now_ms = millis()
        t_s = (now_ms - start_ms) / 1000.0

        pitch_cmd, yaw_cmd = profile(t_s)
        pitch_cmd, pitch_pwm = pitch.command_deg(pitch_cmd)
        yaw_cmd, yaw_pwm = yaw.command_deg(yaw_cmd)
        imu_data = imu.read()

        row = {
            "time_ms": now_ms - start_ms,
            "mode": MODE,
            "pitch_cmd_deg": pitch_cmd,
            "yaw_cmd_deg": yaw_cmd,
            "pitch_pwm_us": pitch_pwm,
            "yaw_pwm_us": yaw_pwm,
        }
        row.update(imu_data)
        print_row(row)
        sleep_dt()


run()
