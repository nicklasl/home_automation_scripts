import argparse
import os
import sys
import time

# Path hack.
sys.path.insert(0, os.path.abspath('..'))

import reporting.influx as influx

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'


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


def report_temperature(current_temperature, report):
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "type": report
            },
            "fields": {
                "value": float(current_temperature)
            }
        }
    ]
    influx.log(json_body, True)


parser = argparse.ArgumentParser(description='Get 1wire temperature and store it.')
parser.add_argument("folder", type=str, help='the sensor folder name (e.g. 28-00000xxxxxxx)')
parser.add_argument("report", type=str, help='the sensor reporting name (e.g. basement)')
args = parser.parse_args()

temperature = read_temp_for_folder(args.folder)
report_temperature(temperature, args.report)
