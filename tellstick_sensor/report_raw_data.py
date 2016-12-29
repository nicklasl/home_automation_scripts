import os
import sys

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import reporting.influx as influx

#class:sensor;protocol:fineoffset;id:135;model:temperaturehumidity;humidity:34;temp:20.2;
#class:sensor; 1
# protocol:fineoffset; 2
# id:135; 3
# model:temperaturehumidity; 4
# humidity:34; 5
# temp:20.2; 6
args = sys.argv[1].split(";") #arg0 is the file.py
print "args={}".format(args)
_type = args[3].split(":")[1]
_id = args[2].split(":")[1]
temperature = args[5].split(":")[1]
humidity = args[4].split(":")[1]

print "type={},id={},temperature={},humidity={}".format(_type, _id, temperature, humidity)

sensor_name = "not_set"

if _type == 'temperaturehumidity' and _id == '135':
    print "temperature:{}, humidity:{}".format(temperature, humidity)
    sensor_name = "inside_1_floor_hallway"
if _type == 'temperaturehumidity' and _id == '167':
    print "temperature:{}, humidity:{}".format(temperature, humidity)
    sensor_name = "inside_basement_storage"

json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "type": sensor_name
        },
        "fields": {
            "value": float(temperature)
        }
    },
    {
        "measurement": "humidity",
        "tags": {
            "type": sensor_name
        },
        "fields": {
            "value": float(humidity)
        }
    }
]

if sensor_name != "not_set":
    influx.log(json_body, True)
