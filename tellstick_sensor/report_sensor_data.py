import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import reporting.influx as influx

#fineoffset;temperaturehumidity;135;1;19.7;1480793818
args = sys.argv[1].split(";") #arg0 is the file.py
_type = args[1]
_id = args[2]
temperature = args[4]
timestamp = args[5]

print "type={},id={},temperature={},timestamp={}".format(_type, _id, temperature,timestamp)

sensor_name = "not_set"

if _type == 'temperaturehumidity' and _id == '135':
    print "temperature:{}".format(temperature)
    sensor_name = "inside_1_floor_hallway"

json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "type": sensor_name
        },
        "fields": {
            "value": float(temperature)
        }
    }
]

influx.log(json_body, True)