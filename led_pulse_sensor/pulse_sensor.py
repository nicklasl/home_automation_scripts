#!/usr/bin/python
import datetime
import os
import sys
import time
import threading


from Adafruit_TSL2561 import Adafruit_TSL2561

# import RPi.GPIO as GPIO

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

HIGH = "HIGH"
LOW = "LOW"
REPORT_PERIOD_SECONDS = 5  # 5 * 60

previous_light_level = LOW
last_report_initiated = 0
pulses = 0


def read_lux():
    try:
        lux = sensor.calculate_lux()
        print "{} = {}".format("lux", lux)
        # lux = datetime.datetime.now().second #debug
        # TODO fix this to measure against a threshold value
        if lux % 2 == 0:
            lux = HIGH
        else:
            lux = LOW
        return lux
    except OverflowError as e:
        print(e)
        #TODO report this somehow!
        return HIGH


def report():
    global last_report_initiated
    global pulses
    last_report_initiated = datetime.datetime.now().second
    # TODO do real reporting
    print "reporting %i pulses" % pulses
    pulses = 0


def handle_control_led(light_level):
    # TODO handle control led
    pass


def report_async():
    thr = threading.Thread(target=report, args=(), kwargs={})
    thr.start()


def loop():
    global previous_light_level
    global pulses
    while True:
        light_level = read_lux()
        handle_control_led(light_level)
        if previous_light_level == HIGH and light_level == LOW:
            pulses += 1
        if datetime.datetime.now().second - last_report_initiated >= REPORT_PERIOD_SECONDS:
            report_async()
        previous_light_level = light_level


def setup():
    global sensor
    global last_report_initiated

    last_report_initiated = datetime.datetime.now().second

    # Initialise the sensor
    sensor = Adafruit_TSL2561()

    # Enable auto gain switching between 1x and 16x
    # Default is False
    sensor.enable_auto_gain(True)


try:
    setup()
    loop()
# Stop on Ctrl+C and clean up
except KeyboardInterrupt:
    # GPIO.cleanup()
    print "exiting"
