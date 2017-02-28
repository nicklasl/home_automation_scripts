import yaml
import paho.mqtt.client as mqtt_client
import paho.mqtt.publish as mqtt_publish
import os
import sys
import time

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor")


def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def read_temp_for_folder(sensor):
    device_file = base_dir + '/' + sensor + '/w1_slave'
    return read_temp(device_file)


def load_cfg():
    global cfg
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


def loop_sensors():
    for sensor in cfg['sensors']:
        id = sensor['id']
        try:
            temperature = float(read_temp_for_folder(id))
            mqtt_publish.single(topic=sensor['name'], payload=temperature, qos=0, retain=False,
                            hostname=cfg['mqtt']['host'],
                            port=cfg['mqtt']['port'], client_id="", keepalive=60, will=None, auth=None, tls=None,
                            protocol=mqtt_client.MQTTv311, transport="tcp")
        except IOError as e:
            print "error is {}".format(e)


load_cfg()
loop_sensors()
print "done"
