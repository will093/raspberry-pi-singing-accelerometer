#!/usr/bin/python

import smbus
import math
import time
import os
from pygame import mixer

from mpu6050 import MPU6050

# Initialise the mixer, load the track to play.
mixer.init()
sound = mixer.Sound('rick-roll.wav')
sound.set_volume(1)
channel = mixer.Channel(1)
channel.play(sound, -1)
channel.pause()
print "Channel initialised"

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

accelerometer = MPU6050(bus, address)

while True:
    xRotation = accelerometer.get_x_rotation()
    print "x rotation: ", xRotation

    if (xRotation > 45):
        channel.unpause()
        time.sleep(4.2)
        channel.pause()

    # Poll the sensor every 0.1 seconds
    time.sleep(0.1)
