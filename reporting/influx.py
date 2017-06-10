import logging
import config
import time
import sys
from requests import exceptions
import influxdb

logger = logging.getLogger(__name__)


def setup_influx_client():
    global client
    INFLUX_URI = config.key("INFLUX_URI")
    INFLUX_USERNAME = config.key("INFLUX_USERNAME")
    INFLUX_PASSWORD = config.key("INFLUX_PASSWORD")
    INFLUX_DATABASE = config.key("INFLUX_DATABASE")
    client = influxdb.InfluxDBClient(INFLUX_URI, 8086, INFLUX_USERNAME, INFLUX_PASSWORD, INFLUX_DATABASE)


setup_influx_client()


def log(json, verbose=False, retry = True):
    append_date_time_tags(json)
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
    logger.error("there was an error: {}\nwhile trying to log: {}".format(e, json))


def append_date_time_tags(json):
    import datetime
    d = datetime.date.today()
    mm = '{0:02d}'.format(d.month)
    yyyy = '{0:4d}'.format(d.year)

    for dicts in json:
        for key, value in dicts.iteritems():
            if key == "tags":
                value['yyyy'] = yyyy
                value['mm'] = mm
                value['yyyymm'] = yyyy + mm


def append_time(json):
    nanotime = int(time.time() * 1000000000L)
    for dict in json:
        if not 'time' in dict:
            dict['time'] = nanotime


def setup_logger():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(message)s', filename='influx.log', level=logging.INFO)
    logging.getLogger(__name__).setLevel(logging.DEBUG)

