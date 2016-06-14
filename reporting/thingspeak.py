import config
import httplib
import urllib
import logging

# originally from https://github.com/seanbechhofer/raspberrypi/blob/master/python/thingspeak.py

KEY = config.key('THINGSPEAK_API_KEY')
logger = logging.getLogger(__name__)


def log(dataToSend, verbose=False):
    dataToSend['api_key'] = KEY
    if verbose:
        print dataToSend
    params = urllib.urlencode(dataToSend)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection("api.thingspeak.com")
    conn.request("POST", "/update", params, headers)
    try:
        response = conn.getresponse()
        if verbose:
            logger.debug("{}, {}".format(response.status, response.reason))
            data = response.read()
            logger.debug(data)
    except Exception:
        import traceback
        logger.error('exception: ' + traceback.format_exc())

    conn.close()

def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)