import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))


import threading
import RPi.GPIO as GPIO
import requests
import time
import yaml
import reporting.udp_reporter as udp_reporter


GPIO.setmode(GPIO.BCM)

# 24 = Blue
basement_door_pin = 24
# 23 = Green
garage_door_pin = 23

debug = False


def load_cfg():
    global cfg
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


def setup():
    global last_basement_door_state, last_garage_door_state, host, port, headers, sleep_time
    last_basement_door_state = True
    last_garage_door_state = True
    host = cfg['api']['host']
    port = cfg['api']['port']
    access_token = cfg['api']['access-token']
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    sleep_time = cfg['sleep_time']
    if debug: print "sleep_time={}".format(sleep_time)
    GPIO.setup(basement_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(garage_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def report(door, friendly_name, state_text):
    try:
        url = 'http://{}:{}/api/states/binary_sensor.{}'.format(host, port, door)
        payload = {"state": state_text, "attributes": {"device_class":"door", "friendly_name": friendly_name}}
        
        if debug: print "sending {} to url: {}".format(payload, url)
        r = requests.post(url, json=payload, headers=headers)
    except IOError as e:
        if debug: print "error is {}".format(e)


def report_async(pin, state):
    if state:
        state_text = "on"
    else:
        state_text = "off"
    door = cfg['door'][pin]
    friendly_name = cfg['friendly-name'][pin]
    thr = threading.Thread(target=report, args=(door, friendly_name, state_text,), kwargs={})
    thr.start()


def loop():
    global last_garage_door_state, last_basement_door_state
    while True:
        if door_open(basement_door_pin) != last_basement_door_state:  # Only report if state has changed.
            report_async(basement_door_pin, door_open(basement_door_pin))
            if debug: print("Basement door state changed.")
        if door_open(garage_door_pin) != last_garage_door_state:  # Only report if state has changed.
            report_async(garage_door_pin, door_open(garage_door_pin))
            if debug: print("Garage door state changed.")

        last_garage_door_state = door_open(garage_door_pin)
        last_basement_door_state = door_open(basement_door_pin)
        time.sleep(sleep_time)


def door_open(pin):
    return not GPIO.input(pin)


try:
    load_cfg()
    setup()
    loop()
# Stop on Ctrl+C and clean up
except KeyboardInterrupt:
    GPIO.cleanup()
    print "exiting"