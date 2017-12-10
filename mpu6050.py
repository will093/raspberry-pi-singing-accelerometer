
import math


class MPU6050:
    """Class modelling an MPU6050 accelerometer."""

    _power_mgmt_1 = 0x6b
    _power_mgmt_2 = 0x6c

    def __init__(self, bus, address):
        self._bus = bus
        self._address = address
        # Wake the 6050 up as it starts in sleep mode
        self._bus.write_byte_data(self._address, self._power_mgmt_1, 0)

    def _read_word_2s_compliment(self, adr):
        """Read 16 bit word of 2s compliment data from the given address."""
        high = self._bus.read_byte_data(self._address, adr)
        low = self._bus.read_byte_data(self._address, adr + 1)
        val = (high << 8) + low
        return val

    def _read_word(self, adr):
        """Read a word of data from the given address in integer form."""
        val = self._read_word_2s_compliment(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def get_x_angular_rotation(self):
        """Angular rotation about x axis in degrees/second."""
        return self._read_word(0x43) / 131

    def get_y_angular_rotation(self):
        """Angular rotation about y axis in degrees/second."""
        return self._read_word(0x45) / 131

    def get_z_angular_rotation(self):
        """Angular rotation about z axis in degrees/second."""
        return self._read_word(0x47) / 131

    def get_x_rotation(self):
        """
        Rotation about the x-axis in degress.

        Calculated using accelerometer only and so only accurate whilst static.
        """
        x = self.get_x_acceleration()
        y = self.get_y_acceleration()
        z = self.get_z_acceleration()
        # http://www.hobbytronics.co.uk/accelerometer-info
        radians = math.atan2(x, math.sqrt((y * y) + (z * z)))
        return math.degrees(radians)

    def get_y_rotation(self):
        """
        Rotation about the y-axis in degrees.

        Calculated using accelerometer only and so only accurate whilst static.
        """
        x = self.get_x_acceleration()
        y = self.get_y_acceleration()
        z = self.get_z_acceleration()
        # http://www.hobbytronics.co.uk/accelerometer-info
        radians = math.atan2(y, math.sqrt((x * x) + (z * z)))
        return math.degrees(radians)

    def get_x_acceleration(self):
        """x acceleration in ms-2"""
        return self._read_word(0x3b) / 16384.0

    def get_y_acceleration(self):
        """y acceleration in ms-2"""
        return self._read_word(0x3d) / 16384.0

    def get_z_acceleration(self):
        """z acceleration in ms-2"""
        return self._read_word(0x3f) / 16384.0
