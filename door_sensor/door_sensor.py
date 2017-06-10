import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

pir_pin = 18
door_pin = 23

GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # activate input with PullUp

while True:
    if GPIO.input(door_pin):
        print("DOOR ALARM!")
    time.sleep(0.5)
