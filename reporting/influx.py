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
    print "pushing to retry queue: {}".format(json)
    q.push(str(json))


def write_retry_queue():
    while q:
        queued_json = eval(q.pop())
        print "trying to log a retry {}".format(queued_json)
        log(queued_json, verbose=True, add_to_retry_queue_if_failed=False)
        time.sleep(1)


def log(json, verbose=False, add_to_retry_queue_if_failed=True):
    write_retry_queue()

    append_time(json)
    if verbose:
        logger.debug("writing:{}".format(json))
    try:
        client.write_points(json)
    except exceptions.ConnectionError as connection_error:
        print "there was an error: {}".format(connection_error)
        logger.error("there was an error: {}".format(connection_error))
        if add_to_retry_queue_if_failed:
            append_to_retry_queue(json)
    except exceptions.ReadTimeout as read_timeout:
        print "there was an error: {}".format(read_timeout)
        logger.error("there was an error: {}".format(read_timeout))
        if add_to_retry_queue_if_failed:
            append_to_retry_queue(json)
    except influxdb.exceptions.InfluxDBServerError as db_error:
        print "there was an error: {}".format(db_error)
        logger.error("there was an error: {}".format(db_error))
        if add_to_retry_queue_if_failed:
            append_to_retry_queue(json)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise


def append_time(json):
    nanotime = int(time.time() * 1000000000L)
    for dict in json:
        if not 'time' in dict:
            print "appending time: {}".format(nanotime)
            dict['time'] = nanotime


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

