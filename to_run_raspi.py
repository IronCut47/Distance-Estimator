from __future__ import print_function
import requests
import json
import cv2
import time

addr = 'http://44.197.200.107:8000/'

####################################################################################################

# 1 --> Left
# 2 --> Back
# 3 --> Right

send_frames_latency = 1
camera_id = 1 
test_url = f'{addr}/get_distance/{str(camera_id)}'
cameras = [0]

####################################################################################################

content_type = 'image/jpeg'
headers = {'content-type': content_type}

while True:
    for camera_id in cameras:
        cap = cv2.VideoCapture(camera_id)
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.png', frame)
            try:
                response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
                print(json.loads(response.text))
            except:
                print("--JSON DECODE")
        cap.release()
        time.sleep(send_frames_latency)