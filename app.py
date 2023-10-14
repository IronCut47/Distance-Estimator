from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from obj_distance_estimator import distance

app = Flask(__name__)

@app.route('/get_distance/<id>', methods=['POST'])
def get_distance(id):
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("result.jpg", img) 
    response = distance(img, id)
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/')
def hello():
    return "hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
