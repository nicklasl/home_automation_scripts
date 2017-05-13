import os
import json
import time
from flask import Flask
import sensor_reader
app = Flask(__name__)

BASE_DIR = '/sys/bus/w1/devices/'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sensors")
def list_sensors():
    dirs = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
    return json.dumps(dirs)

@app.route("/sensors/<id>")
def get_temp_for_sensor(id):
    sensor_file = BASE_DIR + id + '/w1_slave'
    temperature = sensor_reader.read_temp(sensor_file)
    result = {"id": id,
     "temperature": temperature,
     "timestamp": time.time()}
    return json.dumps(result)


if __name__ == "__main__":
    if os.getuid() != 0:
        print "This server needs to be run as root. Sorry!"
        exit(1)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    app.run(host='0.0.0.0')