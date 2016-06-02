import config
import httplib
import urllib

# originally from https://github.com/seanbechhofer/raspberrypi/blob/master/python/thingspeak.py

KEY = config.key('THINGSPEAK_API_KEY')


# print KEY

def log(dataToSend, verbose=False):
    dataToSend['api_key'] = KEY
    if verbose:
        print dataToSend
    params = urllib.urlencode(dataToSend)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPSConnection("api.thingspeak.com")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    if verbose:
        print response.status, response.reason
    data = response.read()
    conn.close()
