import logging
import config
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)
INFLUX_URI = config.key("INFLUX_URI")
client = InfluxDBClient(INFLUX_URI, 8086, 'root', 'root', 'home')


def log(pulses, k_w_h, verbose=False):
    json_body = [
        {
            "measurement": "electricity",
            "tags": {
                "type": "kwh"
            },
            "fields": {
                "value": float(k_w_h)
            }
        },
        {
            "measurement": "electricity",
            "tags": {
                "type": "pulses"
            },
            "fields": {
                "value": float(pulses)
            }
        }
    ]
    if verbose:
        logger.debug("writing:{}".format(json_body))

    client.write_points(json_body)


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

