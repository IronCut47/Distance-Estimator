from __future__ import print_function
import requests
import json
import cv2
import time

addr = 'http://localhost:5000' # to change

test_url = f'{addr}/get_distance/1'

content_type = 'image/jpeg'
headers = {'content-type': content_type}

cameras = [0]

while True:
    for camera_id in cameras:
        cap = cv2.VideoCapture(camera_id)
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.png', frame)
            response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
            print(json.loads(response.text))
        cap.release()
        time.sleep(1)