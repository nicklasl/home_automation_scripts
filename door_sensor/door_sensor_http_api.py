import json

import yaml
from flask import Flask
from gpiozero import Button

app = Flask(__name__)

basement_door_pin = 24
garage_door_pin = 23
garage = Button(basement_door_pin)
basement = Button(garage_door_pin)


@app.route("/state")
def get_state():
    return json.dumps([
        {'door': cfg['door'][basement_door_pin],
         'open': not basement.is_pressed},
        {'door': cfg['door'][garage_door_pin],
         'open': not garage.is_pressed}
    ])


def load_cfg():
    global cfg
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


if __name__ == "__main__":
    load_cfg()
    app.run(host='0.0.0.0', port=5001)
