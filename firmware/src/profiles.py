"""Open-loop command profiles for Rev A bench tests."""

import math

from config import STEP_AMPLITUDE_DEG, STEP_PERIOD_S, SWEEP_AMPLITUDE_DEG, SWEEP_PERIOD_S


def neutral_profile(_t_s):
    return 0.0, 0.0


def sweep_pitch_profile(t_s):
    pitch = SWEEP_AMPLITUDE_DEG * math.sin(2.0 * math.pi * t_s / SWEEP_PERIOD_S)
    return pitch, 0.0


def sweep_yaw_profile(t_s):
    yaw = SWEEP_AMPLITUDE_DEG * math.sin(2.0 * math.pi * t_s / SWEEP_PERIOD_S)
    return 0.0, yaw


def step_pitch_profile(t_s):
    phase = int(t_s / STEP_PERIOD_S) % 2
    pitch = STEP_AMPLITUDE_DEG if phase == 0 else -STEP_AMPLITUDE_DEG
    return pitch, 0.0


def step_yaw_profile(t_s):
    phase = int(t_s / STEP_PERIOD_S) % 2
    yaw = STEP_AMPLITUDE_DEG if phase == 0 else -STEP_AMPLITUDE_DEG
    return 0.0, yaw


PROFILES = {
    "neutral": neutral_profile,
    "sweep_pitch": sweep_pitch_profile,
    "sweep_yaw": sweep_yaw_profile,
    "step_pitch": step_pitch_profile,
    "step_yaw": step_yaw_profile,
}
