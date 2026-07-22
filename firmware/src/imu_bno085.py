"""BNO085 interface placeholder.

Prototype 1 starts with safe servo bring-up even before the IMU driver is
installed. This class preserves the telemetry contract so data-analysis scripts
do not need to change when the real BNO085 driver is added.
"""

try:
    from machine import I2C, Pin
except ImportError:
    I2C = None
    Pin = None

from config import BNO085_I2C_ADDR_CANDIDATES, I2C_FREQ_HZ, I2C_SCL_PIN, I2C_SDA_PIN


class BNO085:
    def __init__(self):
        self.present = False
        self.address = None
        self._i2c = None

        if I2C is not None:
            self._i2c = I2C(
                0,
                sda=Pin(I2C_SDA_PIN),
                scl=Pin(I2C_SCL_PIN),
                freq=I2C_FREQ_HZ,
            )
            addresses = set(self._i2c.scan())
            for candidate in BNO085_I2C_ADDR_CANDIDATES:
                if candidate in addresses:
                    self.present = True
                    self.address = candidate
                    break

    def read(self):
        """Return attitude/rate fields with stable names.

        Real BNO085 quaternion and gyro reads will replace these placeholders.
        """
        return {
            "imu_present": int(self.present),
            "quat_w": 1.0,
            "quat_x": 0.0,
            "quat_y": 0.0,
            "quat_z": 0.0,
            "gyro_x_dps": 0.0,
            "gyro_y_dps": 0.0,
            "gyro_z_dps": 0.0,
        }
