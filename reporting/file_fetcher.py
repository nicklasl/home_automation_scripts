import argparse
import os
from datetime import datetime
import reporting.influx as influx
try: import simplejson as json
except ImportError: import json


FILE_NAME_SUFFIX = ".measurement"
FOLDER = "/tmp/measurements/"
LOCAL_FOLDER = "./measurements/"

parser = argparse.ArgumentParser(description='Fetch file to report.')
parser.add_argument("server", type=str, help='the server to fetch from')
parser.add_argument("user", type=str, help='the user name')
args = parser.parse_args()

if not os.path.isdir(LOCAL_FOLDER):
    os.makedirs(LOCAL_FOLDER)

now = datetime.now()
file_name = now.strftime("%Y-%m-%d") + FILE_NAME_SUFFIX
cmd = "scp {}@{}:{} {}".format(args.user, args.server, FOLDER + file_name, LOCAL_FOLDER)
print cmd
os.system(cmd)

if os.path.isfile(LOCAL_FOLDER + file_name):
    with open(LOCAL_FOLDER + file_name) as f:
        contents = f.readlines()
        result = []
        for outer_arr in contents:
            for inner_arr in eval(outer_arr.replace("'", '"').replace("L,", ",")):
                result.append(inner_arr)
        influx.log(result)