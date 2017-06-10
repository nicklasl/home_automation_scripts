import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#24 = Blue
basement_door_pin = 24
#23 = Green
garage_door_pin = 23

GPIO.setup(basement_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(garage_door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    if GPIO.input(basement_door_pin):
        print("BASEMENT DOOR ALARM!")
    if GPIO.input(garage_door_pin):
        print("GARAGE_DOOR_ALARM")
    time.sleep(2)