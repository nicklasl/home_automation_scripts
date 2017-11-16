from Arlo import Arlo
import config

USERNAME = config.key("ARLO_USERNAME")
PASSWORD = config.key("ARLO_PASSWORD")

try:
    arlo = Arlo(USERNAME, PASSWORD)
    basestations = arlo.GetDevices('basestation')

    arlo.Arm(basestations[0])
except Exception as e:
    print(e)