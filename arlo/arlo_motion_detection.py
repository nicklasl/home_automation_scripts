from Arlo import Arlo
import config
import os
from subprocess import call

USERNAME = config.key("ARLO_USERNAME")
PASSWORD = config.key("ARLO_PASSWORD")

MOTION_DETECT_ACTION_SCRIPT = "curl.sh"

try:
    arlo = Arlo(USERNAME, PASSWORD)
    basestations = arlo.GetDevices('basestation')

    # Define a callback function that will get called once for each motion event.
    def callback(arlo, basestation, event):
        # Here you will have access to self, basestation_id, xcloud_id, and the event schema.
        print("motion event detected!")
        print(event)
        print(basestation)
        if os.path.isfile(MOTION_DETECT_ACTION_SCRIPT):
            call(['bash', MOTION_DETECT_ACTION_SCRIPT, "camera id"])
        #print(arlo)

    # Subscribe to motion events. This method blocks until the event stream is closed. (You can close the event stream in the callback if you no longer want to listen for events.)
    arlo.SubscribeToMotionEvents(basestations[0], callback)
except Exception as e:
    print(e)