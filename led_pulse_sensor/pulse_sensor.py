#!/usr/bin/python
import datetime
import os
import sys
import time
import threading

from Adafruit_TSL2561 import Adafruit_TSL2561

import RPi.GPIO as GPIO

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

LUX_THRESHOLD = 5
HIGH = "HIGH"
LOW = "LOW"
REPORT_PERIOD_SECONDS = 5  # 5 * 60
LED_PIN = 18

previous_light_level = LOW
last_report_initiated = 0
pulses = 0


def read_lux():
    try:
        lux = sensor.calculate_lux()
        print "{} = {}".format("lux", lux)
        if lux > LUX_THRESHOLD:
            lux = HIGH
        else:
            lux = LOW
    except OverflowError as e:
        print(e)
        # TODO report this somehow!
        lux = HIGH
    return lux


def report():
    global last_report_initiated
    global pulses
    last_report_initiated = datetime.datetime.now().second
    # TODO do real reporting
    print "reporting %i pulses" % pulses
    pulses = 0


def handle_control_led(light_level):
    if light_level == HIGH:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


def report_async():
    thr = threading.Thread(target=report, args=(), kwargs={})
    thr.start()


def loop():
    global previous_light_level
    global pulses
    while True:
        current_light_level = read_lux()
        handle_control_led(current_light_level)
        if previous_light_level == HIGH and current_light_level == LOW:
            print "registering pulse"
            pulses += 1
        if datetime.datetime.now().second - last_report_initiated >= REPORT_PERIOD_SECONDS:
            report_async()
        previous_light_level = current_light_level


def setup():
    global sensor
    global last_report_initiated

    last_report_initiated = datetime.datetime.now().second

    # Initialise the sensor
    sensor = Adafruit_TSL2561()

    # Enable auto gain switching between 1x and 16x
    # Default is False
    sensor.enable_auto_gain(True)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)


try:
    setup()
    loop()
    # Stop on Ctrl+C and clean up
except KeyboardInterrupt:
    GPIO.cleanup()
    print "exiting"
