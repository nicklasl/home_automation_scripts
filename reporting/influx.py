import logging
import config
import time
import sys
from requests import exceptions
import influxdb
from queuelib import FifoDiskQueue

logger = logging.getLogger(__name__)
INFLUX_URI = config.key("INFLUX_URI")
client = influxdb.InfluxDBClient(INFLUX_URI, 8086, 'root', 'root', 'home')
q = FifoDiskQueue("queuefile")


def append_to_retry_queue(json):
    q.push(str(json))


def write_retry_queue():
    while q:
        queued_json = eval(q.pop())
        log(queued_json, verbose=True, retry = False)
        time.sleep(1)


def log(json, verbose=False, retry = True):
    if retry:
        write_retry_queue()

    append_time(json)
    if verbose:
        logger.debug("writing:{}".format(json))
    try:
        client.write_points(json)
    except exceptions.ConnectionError as connection_error:
        handle_error(connection_error, json)
    except exceptions.ReadTimeout as read_timeout:
        handle_error(read_timeout, json)
    except influxdb.exceptions.InfluxDBServerError as db_error:
        handle_error(db_error, json)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def handle_error(e, json):
    logger.error("there was an error: {}".format(e))
    append_to_retry_queue(json)


def append_time(json):
    nanotime = int(time.time() * 1000000000L)
    for dict in json:
        if not 'time' in dict:
            dict['time'] = nanotime


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

