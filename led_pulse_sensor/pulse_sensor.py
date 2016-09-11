#!/usr/bin/python
from __future__ import division

import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import logging
import reporting.influx as influx
from datetime import datetime
import threading
import RPi.GPIO as GPIO
from Adafruit_TSL2561 import Adafruit_TSL2561

LUX_THRESHOLD = 1
HIGH = "HIGH"
LOW = "LOW"
REPORT_PERIOD_SECONDS = 5 * 60
MULTIPLIER_K_W_H = 3600 / REPORT_PERIOD_SECONDS / 1000
LED_PIN = 18

logger = logging.getLogger(__name__)
previous_light_level = LOW
last_report_initiated = datetime.now()
pulses = 0


def read_lux():
    try:
        lux_value = sensor.calculate_lux()
        if lux_value > LUX_THRESHOLD:
            #logger.debug("lux = {}".format(lux_value))
            lux = HIGH
        else:
            lux = LOW
    except OverflowError as e:
        logger.error(e)
        # TODO report this somehow!
        lux = HIGH
    return lux


def report(pulses_to_report, kwh_to_report):
    json_body = [
        {
            "measurement": "electricity",
            "tags": {
                "type": "kwh"
            },
            "fields": {
                "value": float(kwh_to_report)
            }
        },
        {
            "measurement": "electricity",
            "tags": {
                "type": "pulses"
            },
            "fields": {
                "value": float(pulses_to_report)
            }
        }
    ]
    influx.log(json_body, True)


def handle_control_led(light_level):
    if light_level == HIGH:
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)


def report_async():
    global last_report_initiated
    global pulses
    k_w_h = pulses * MULTIPLIER_K_W_H
    thr = threading.Thread(target=report, args=(pulses, k_w_h,), kwargs={})
    thr.start()
    pulses = 0
    last_report_initiated = datetime.now()


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
        if should_report():
            report_async()

        previous_light_level = current_light_level


def setup():
    logging.basicConfig(format='%(asctime)s %(message)s', filename='pulse_sensor.log',level=logging.ERROR)
    logging.getLogger(__name__).setLevel(logging.DEBUG)

    influx.setup_logger()

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



