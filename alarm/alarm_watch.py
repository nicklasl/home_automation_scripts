#!/usr/bin/python
import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import influxdb
import config
import logging

LIMIT = 1600

def setup_logging():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', filename='alarm.log', level=logging.INFO)
    logging.getLogger(__name__).setLevel(logging.DEBUG)


def setup_influx_client():
    global client
    INFLUX_URI = config.key("INFLUX_URI")
    INFLUX_USERNAME = config.key("INFLUX_USERNAME")
    INFLUX_PASSWORD = config.key("INFLUX_PASSWORD")
    INFLUX_DATABASE = config.key("INFLUX_DATABASE")
    client = influxdb.InfluxDBClient(INFLUX_URI, 8086, INFLUX_USERNAME, INFLUX_PASSWORD, INFLUX_DATABASE)


def main():
    result = client.query('select sum(value) from electricity where time > now() - 15m')
    dict = result.raw
    watts_last_15m = dict[u'series'][0][u'values'][0][1]
    print watts_last_15m
    if watts_last_15m > LIMIT:
        logger.warn("more than {} w per hour. Consumed last 15 min: {}".format(LIMIT * 4, watts_last_15m))
    else:
        logger.debug("Consumed last 15 min: {} W".format(watts_last_15m))


setup_logging()
setup_influx_client()

main()
