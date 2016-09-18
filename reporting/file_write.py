import logging
import time
from datetime import datetime
import os

logger = logging.getLogger(__name__)
FILE_NAME_SUFFIX = ".measurement"
FOLDER = "measurements"

def write_append(file_name, json):
    with open(file_name, "a+") as myfile:
        myfile.write(str(json) + "\n")


def log(json, verbose=False):
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    file_name = FOLDER + os.path.sep + datetime.now().strftime("%Y-%m-%d") + FILE_NAME_SUFFIX
    append_time(json)
    if verbose:
        logger.debug("writing to file {}:{}".format(file_name, json))
    write_append(file_name, json)


def append_time(json):
    nanotime = int(time.time() * 1000000000L)
    for dict in json:
        if not 'time' in dict:
            dict['time'] = nanotime


def setup_logger():
    logging.getLogger(__name__).setLevel(logging.DEBUG)

