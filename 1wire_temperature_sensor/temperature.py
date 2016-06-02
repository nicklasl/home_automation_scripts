import datetime
import glob
import os
import time

import thingspeak

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')

result = []


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def append_to_file(arg):
    hs = open("/tmp/temps.log", "a")
    for line in arg:
        hs.write(line + "\n")
    hs.close()


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


for device_folder in device_folders:
    device_file = device_folder + '/w1_slave'
    now = datetime.datetime.today().isoformat()
    temp = read_temp()
    thingspeak.log({'field1': str(temp)}, True)
    result.append(device_file + " --- " + now + " --- " + str(temp))

print(result)
# append_to_file(result)
