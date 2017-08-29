import threading

import RPi.GPIO as GPIO
import requests
import time
import yaml
import reporting.udp_alive_reporter as udp_reporter


GPIO.setmode(GPIO.BCM)

# 24 = Blue
basement_door_pin = 24
# 23 = Green
garage_door_pin = 23

debug = True


def load_cfg():
    global cfg
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


def setup():
    global last_basement_door_state, last_garage_door_state, url, sleep_time
    last_basement_door_state = True
    last_garage_door_state = True
    host = cfg['api']['host']
    port = cfg['api']['port']
    url = 'http://{}:{}/doorsensor'.format(host, port)
    sleep_time = cfg['sleep_time']
    if debug: print "url={}".format(url)
    if debug: print "sleep_time={}".format(sleep_time)
    GPIO.setup(basement_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(garage_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def report(door, state_text):
    try:
        blob = {'door': door, 'state': state_text}
        if debug: print "sending to server: {}".format(blob)
        r = requests.post(url, data=blob)
    except IOError as e:
        if debug: print "error is {}".format(e)


def report_async(pin, state):
    if state:
        state_text = "open"
    else:
        state_text = "closed"
    door = cfg['door'][pin]
    thr = threading.Thread(target=report, args=(door, state_text,), kwargs={})
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
    return GPIO.input(pin)


try:
    load_cfg()
    setup()
    udp_reporter.start_reporting("door_sensor.py")
    loop()
# Stop on Ctrl+C and clean up
except KeyboardInterrupt:
    GPIO.cleanup()
    print "exiting"
