from __future__ import print_function
from json.decoder import JSONDecodeError
import requests
import json
import cv2
import time

addr = 'http://44.197.200.107:8000/'

####################################################################################################

# 1 --> Left
# 0 --> Back
# 3 --> Right

send_frames_latency = 1
camera_id = 1 
test_url = f'{addr}/get_distance/{str(camera_id)}'

test_cameras = {0: "back"}
cameras = {0: "back", 1 : "left", 2 : "right"}

####################################################################################################

content_type = 'image/jpeg'
headers = {'content-type': content_type}

while True:
    for camera_id in list(test_cameras.keys()):
        cap = cv2.VideoCapture(camera_id)
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.png', frame)
            try:
                response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
                print(json.loads(response.text), "Camera NAME", test_cameras[camera_id])
            except JSONDecodeError:
                print("-->JSON DECODE")
        cap.release()
        time.sleep(send_frames_latency)