from __future__ import print_function
from json.decoder import JSONDecodeError
import requests
import json
import cv2
import time
from motor_run import run_both_motors,run_left_motor,run_right_motor


addr = 'http://192.168.182.191:8000/'

####################################################################################################

# 1 --> Left
# 0 --> Back
# 3 --> Right

send_frames_latency = 0.3
camera_id = 1 
test_url = f'{addr}/get_distance/{str(camera_id)}'

test_cameras = {0: "back"}
cameras = {0: "back", 1 : "right", 2 : "left"}

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
                response_raw = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
                response = json.loads(response_raw.text)
                if response['data'] != []:
                    for obj in response['data']:
                        if 'detected' in obj.keys():
                            print(obj['id'], obj['class'], obj['distance'], "-->" ,obj['detected'], obj['id'])
                            #motor run left if id is 1
                            if obj['id'] == '1':
                                run_right_motor()
                            if obj['id'] == '2':
                                run_left_motor()
                            if obj['id'] == '0':
                                run_both_motors()
            except JSONDecodeError:
                print("-->JSON DECODE")
        cap.release()
        time.sleep(send_frames_latency)