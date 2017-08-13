import json

import time
from flask import Flask, abort

import sensor_reader

app = Flask(__name__)

SENSORS = [
    {'id': "1",
     'friendlyName': "inside_basement_storage",
     'gpioPin': 4},
    {'id': "2",
     'friendlyName': "outside_conservatory",
     'gpioPin': 17}]


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sensors")
def list_sensors():
    return json.dumps(SENSORS)


@app.route("/sensors/<id>")
def get_temp_for_sensor(id):
    sensor_to_check = next((sensor for sensor in SENSORS if sensor["id"] == id), None)
    if not sensor_to_check:
        return abort(404)

    temperature, humidity = sensor_reader.read_temp_and_humidity(sensor_to_check["gpioPin"])
    result = {"id": id,
              "friendlyName": sensor_to_check["friendlyName"],
              "temperature": temperature,
              "humidity": humidity,
              "timestamp": time.time()}
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
