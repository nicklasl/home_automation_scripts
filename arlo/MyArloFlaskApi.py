import datetime
import json
from datetime import timedelta, date
import threading
from flask import Flask
from flask import request

import config
from Arlo import Arlo

app = Flask(__name__)

USERNAME = config.key("ARLO_USERNAME")
PASSWORD = config.key("ARLO_PASSWORD")
translator = {"kitchen": "4N7171S9253E0",
              "hallway": "4WA16C7UD0048",
              "living_room": "4WA16C76D1B5C"}


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/arm", methods=['POST'])
def arm_request():
    result = arlo.Arm(basestation)
    return json.dumps(result)


@app.route("/disarm", methods=['POST'])
def disarm_request():
    result = arlo.Disarm(basestation)
    return json.dumps(result)


@app.route("/camera")
def cameras():
    camera_list = arlo.GetDevices('camera')
    return json.dumps(camera_list)


def camera_for_device_id(camera_device_id):
    camera_list = arlo.GetDevices('camera')
    camera = (item for item in camera_list if item["deviceId"] == camera_device_id).next()
    return camera


@app.route("/camera/record", methods=['POST'])
def record():
    camera_name = request.args.get('cameraname')
    camera_device_id = translator[camera_name]
    print("camera_device_id={}".format(camera_device_id))
    camera = camera_for_device_id(camera_device_id)
    result = arlo.StartRecording(camera)
    return json.dumps(result)


@app.route("/download", methods=['POST'])
def download_videos_last_24h():
    today = (date.today() - timedelta(days=0)).strftime("%Y%m%d")
    yesterday = (date.today() - timedelta(hours=24)).strftime("%Y%m%d")
    print("today={}, yesterday={}".format(today, yesterday))
    library = arlo.GetLibrary(yesterday, today)
    # Iterate through the recordings in the library.
    for recording in library:
        videofilename = datetime.datetime.fromtimestamp(int(recording['name']) // 1000).strftime(
            '%Y-%m-%d %H-%M-%S') + ' ' + recording['uniqueId'] + '.mp4'
        ##
        # The videos produced by Arlo are pretty small, even in their longest, best quality settings,
        # but you should probably prefer the chunked stream (see below).
        ###
        #    # Download the whole video into memory as a single chunk.
        video = arlo.GetRecording(recording['presignedContentUrl'])
        with open('videos/' + videofilename, 'w') as f:
            f.write(video)
            f.close()
        # Or:
        #
        # Get video as a chunked stream; this function returns a generator.
        # stream = arlo.StreamRecording(recording['presignedContentUrl'])
        # with open('videos/' + videofilename, 'w') as f:
        #     for chunk in stream:
        #         # Support both Python 2.7 and 3.
        #         if sys.version[0] == '2':
        #             f.write(chunk)
        #         else:
        #             f.buffer.write(chunk)
        #     f.close()

        print('Downloaded video ' + videofilename + ' from ' + recording['createdDate'] + '.')

    # Delete all of the videos you just downloaded from the Arlo library.
    # Notice that you can pass the "library" object we got back from the GetLibrary() call.
    if len(library) > 0:
        result = arlo.BatchDeleteRecordings(library)
        print('Batch deletion of videos completed successfully.')

    return "ok"


if __name__ == "__main__":
    arlo = Arlo(USERNAME, PASSWORD)
    basestation = arlo.GetDevices('basestation')[0]
    # download_videos_last_24h()
    app.run(host='0.0.0.0')
