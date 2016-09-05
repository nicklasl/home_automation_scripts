import logging
import config
import time
from requests import exceptions
from influxdb import InfluxDBClient
from queuelib import FifoDiskQueue

logger = logging.getLogger(__name__)
INFLUX_URI = config.key("INFLUX_URI")
client = InfluxDBClient(INFLUX_URI, 8086, 'root', 'root', 'home')
q = FifoDiskQueue("queuefile")


def append_to_retry_queue(json):
    q.push(json)


def write_retry_queue():
    while q:
        log(q.pop(), verbose=True)


def log(json, verbose=False):
    write_retry_queue()

    append_time(json)
    if verbose:
        logger.debug("writing:{}".format(json))
    try:
        client.write_points(json)
    except exceptions.ConnectionError as e:
        logger.error( "there was an error: {}".format(e))
        append_to_retry_queue(json)


def append_time(json):
    nanotime = int(time.time() * 1000000000L)
    for dict in json:
        if not 'time' in dict:
            dict['time'] = nanotime


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

