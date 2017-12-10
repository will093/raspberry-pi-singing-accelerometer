#!/usr/bin/python

import unittest
from unittest.mock import Mock
from mpu6050 import MPU6050


class MPU6050Tests(unittest.TestCase):

    def setUp(self):
        self.testAddress = 0x68
        self.testBus = Mock()
        self.testBus.read_byte_data.return_value = 0x00
        self.accelerometer = MPU6050(self.testBus, self.testAddress)

    def test_init_should_wake_up_mpu(self):
        self.testBus.write_byte_data.assert_called_with(
            self.testAddress, 0x6b, 0)

    def test_get_x_angular_rotation_correct_positive_angular_rotation(self):
        self.testBus.read_byte_data.side_effect = [0x01, 0x06]
        expected = self.accelerometer.get_x_angular_rotation()
        self.assertEqual(expected, 2)

    def test_get_x_angular_rotation_correct_negative_angular_rotation(self):
        # Return 2s complement value of -262
        self.testBus.read_byte_data.side_effect = [0xfe, 0xfa]
        expected = self.accelerometer.get_x_angular_rotation()
        self.assertEqual(expected, -2)

    def test_get_x_angular_rotation_correct_zero_angular_rotation(self):
        # Return 2s complement value of -262
        self.testBus.read_byte_data.side_effect = [0x00, 0x00]
        expected = self.accelerometer.get_x_angular_rotation()
        self.assertEqual(expected, 0)

    def test_get_x_angular_rotation_correct_pin(self):
        self.accelerometer.get_x_angular_rotation()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x43)

    def test_get_y_angular_rotation_correct_pin(self):
        self.accelerometer.get_y_angular_rotation()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x45)

    def test_get_z_angular_rotation_correct_pin(self):
        self.accelerometer.get_z_angular_rotation()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x47)

    def test_get_x_acceleration_correct_pin(self):
        self.accelerometer.get_x_acceleration()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x3b)

    def test_get_y_acceleration_correct_pin(self):
        self.accelerometer.get_y_acceleration()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x3d)

    def test_get_z_acceleration_correct_pin(self):
        self.accelerometer.get_z_acceleration()
        self.testBus.read_byte_data.assert_any_call(self.testAddress, 0x3f)

    def test_get_z_acceleration_correct_acceleration(self):
        # Return 2s complement value of 16384
        self.testBus.read_byte_data.side_effect = [0x40, 0x00]
        expected = self.accelerometer.get_z_acceleration()
        self.assertEqual(expected, 1)

    def test_get_y_rotation_correct_rotation(self):
        self.accelerometer.get_x_acceleration = Mock()
        self.accelerometer.get_x_acceleration.return_value = 5
        self.accelerometer.get_y_acceleration = Mock()
        self.accelerometer.get_y_acceleration.return_value = 3
        self.accelerometer.get_z_acceleration = Mock()
        self.accelerometer.get_z_acceleration.return_value = 4
        expected = self.accelerometer.get_x_rotation()
        self.assertEqual(expected, 45)

    def test_get_x_rotation_correct_rotation(self):
        self.accelerometer.get_x_acceleration = Mock()
        self.accelerometer.get_x_acceleration.return_value = -3
        self.accelerometer.get_y_acceleration = Mock()
        self.accelerometer.get_y_acceleration.return_value = 5
        self.accelerometer.get_z_acceleration = Mock()
        self.accelerometer.get_z_acceleration.return_value = -4
        expected = self.accelerometer.get_y_rotation()
        self.assertEqual(expected, 45)
