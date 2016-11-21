#!/usr/bin/python
# coding=utf-8
# Loads of inspiration taken from https://github.com/erijo/tellcore-py
import os
import sys
# Path hack.
sys.path.insert(0, os.path.abspath('..'))
from subprocess import call
import logging
import tellcore_loop
from tellcore.telldus import TelldusCore


PUSH_NOTIFICATION_FILE_NAME = "../send_push.sh"


def setup_logging():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', filename='events.log', level=logging.INFO)
    logging.getLogger(__name__).setLevel(logging.DEBUG)


def send_push(title, text):
    if os.path.isfile(PUSH_NOTIFICATION_FILE_NAME):
        call(['bash', PUSH_NOTIFICATION_FILE_NAME, title, text])


def my_func(device_id, method_string):
    device = get_device_from_id(device_id)
    if device.name is "Back door" and method_string is "turn on":
       send_push("Pling plong!", "Dörren till glasrummet öppnades.")


def get_device_from_id(id):
    return iter(filter(lambda device: device.id == id, core.devices())).next()


def main():
    device_door = ("device", my_func)
    tellcore_loop.add_events([device_door])
    tellcore_loop.start()

core = TelldusCore()
setup_logging()
main()
