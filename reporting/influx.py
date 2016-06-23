import logging
import config
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)
INFLUX_URI = config.key("INFLUX_URI")
client = InfluxDBClient(INFLUX_URI, 8086, 'root', 'root', 'home')


def log(json, verbose=False):
    if verbose:
        logger.debug("writing:{}".format(json))
    client.write_points(json)


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

