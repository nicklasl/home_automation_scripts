#!/usr/bin/python

import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import logging

import reporting.thingspeak as thingspeak
from datetime import datetime
import threading
import RPi.GPIO as GPIO
from Adafruit_TSL2561 import Adafruit_TSL2561

LUX_THRESHOLD = 5
HIGH = "HIGH"
LOW = "LOW"
REPORT_PERIOD_SECONDS = 5 * 60
LED_PIN = 18

logger = logging.getLogger(__name__)
previous_light_level = LOW
last_report_initiated = datetime.now()
pulses = 0


def read_lux():
    try:
        lux_value = sensor.calculate_lux()
        if lux_value > LUX_THRESHOLD:
            logger.debug("lux = {}".format(lux_value))
            lux = HIGH
        else:
            lux = LOW
    except OverflowError as e:
        logger.error(e)
        # TODO report this somehow!
        lux = HIGH
    return lux


def report(data):
    logger.info("reporting pulses = {}".format(data))
    thingspeak.log(data, False)


def handle_control_led(light_level):
    if light_level == HIGH:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


def report_async():
    global last_report_initiated
    global pulses
    logger.debug("Reporting at {}. Last report was {}".format(datetime.now(), last_report_initiated))
    data = {'field3': str(pulses)}
    pulses = 0
    last_report_initiated = datetime.now()
    thr = threading.Thread(target=report, args=data, kwargs={})
    thr.start()


def should_report():
    return (datetime.now() - last_report_initiated).total_seconds() > REPORT_PERIOD_SECONDS


def loop():
    global previous_light_level
    global pulses
    while True:
        current_light_level = read_lux()
        handle_control_led(current_light_level)
        if previous_light_level == HIGH and current_light_level == LOW:
            pulses += 1
            logger.debug("registering pulse. ({})".format(pulses))
        if should_report():
            report_async()

        previous_light_level = current_light_level


def setup():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='pulse_sensor.log',level=logging.ERROR)
    logging.getLogger(__name__).setLevel(logging.DEBUG)

    global sensor
    global last_report_initiated
    last_report_initiated = datetime.now()

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



