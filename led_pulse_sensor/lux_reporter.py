#!/usr/bin/python

from __future__ import print_function
from Adafruit_TSL2561 import Adafruit_TSL2561
import sys, os

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import reporting.thingspeak as thingspeak

# Initialise the sensor
LightSensor = Adafruit_TSL2561()

# Enable auto gain switching between 1x and 16x
# Default is False
LightSensor.enable_auto_gain(True)

# Get the calculated lux value, this is a spot reading so if you're under light
try:
    lux = LightSensor.calculate_lux()
    thingspeak.log({'field2': str(lux)}, True)
except OverflowError as e:
    print(e)
else:
    print("Lux value is ", lux)
