import cv2 as cv

KNOWN_DISTANCE = 45  # INCHES
PERSON_WIDTH = 16  # INCHES
MOBILE_WIDTH = 3.0  # INCHES
CAR_LENGTH = 200

CONFIDENCE_THRESHOLD = 0.4
NMS_THRESHOLD = 0.3

COLORS = [(255, 0, 0), (255, 0, 255), (0, 255, 255),
          (255, 255, 0), (0, 255, 0), (255, 0, 0)]
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
distance_throshold = 50

FONTS = cv.FONT_HERSHEY_COMPLEX

class_names = []
with open("static/classes.txt", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

yoloNet = cv.dnn.readNet(
    'pretrained_model/yolov4-tiny.weights', 'pretrained_model/yolov4-tiny.cfg')

yoloNet.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
yoloNet.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)

model = cv.dnn_DetectionModel(yoloNet)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)


def object_detector(image):
    classes, scores, boxes = model.detect(
        image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    data_list = []
    for (classid, score, box) in zip(classes, scores, boxes):
        color = COLORS[int(classid) % len(COLORS)]

        label = "%s : %f" % (class_names[classid], score)

        cv.rectangle(image, box, color, 2)
        cv.putText(image, label, (box[0], box[1]-14), FONTS, 0.5, color, 2)

        if classid in [0, 2, 67]:  # Person, car, mobile phone
            data_list.append(
                [class_names[classid], box[2], (box[0], box[1]-2)])

    return data_list


def focal_length_finder(measured_distance, real_width, width_in_rf):
    return (width_in_rf * measured_distance) / real_width


def distance_finder(focal_length, real_object_width, width_in_frmae):
    return (real_object_width * focal_length) / width_in_frmae


ref_person = cv.imread('ReferenceImages/image14.png')
ref_mobile = cv.imread('ReferenceImages/image4.png')
ref_car = cv.imread('ReferenceImages/test.png')

person_data = object_detector(ref_person)
person_width_in_rf = person_data[0][1]

mobile_data = object_detector(ref_mobile)
mobile_width_in_rf = mobile_data[1][1]

car_data = object_detector(ref_car)
# print(car_data)
car_width_in_rf = car_data[0][1]
# print(car_width_in_rf)

focal_car = focal_length_finder(KNOWN_DISTANCE, CAR_LENGTH, car_width_in_rf)
focal_person = focal_length_finder(
    KNOWN_DISTANCE, PERSON_WIDTH, person_width_in_rf)
focal_mobile = focal_length_finder(
    KNOWN_DISTANCE, MOBILE_WIDTH, mobile_width_in_rf)


def distance(frame, id):
    data = object_detector(frame)
    final_response = []
    response = {'detected': False, 'id': id}
    for d in data:
        if d[0] == 'person':
            distance_og = distance_finder(focal_person, PERSON_WIDTH, d[1])
            distance = round(distance_og)
            response['class'] = 'person'
            response['distance'] = distance
            if distance < distance_throshold:
                response['detected'] = True
                response['id'] = id
            x, y = d[2]
            final_response.append(response)
        if d[0] == 'cell phone':
            distance_og = distance_finder(focal_mobile, MOBILE_WIDTH, d[1])
            distance = round(distance_og)
            response['class'] = 'cell phone'
            response['distance'] = distance
            if distance < distance_throshold:
                response['detected'] = True
                response['id'] = id
            x, y = d[2]
            final_response.append(response)
        # elif d[0] =='car':
        #     distance = distance_finder(focal_car, CAR_LENGTH, d[1])
        #     response['class'] = 'car'
        #     response['distance'] = distance
        #     if distance < 50:
        #         response['detected'] = True
        #     x, y = d[2]

        cv.rectangle(frame, (x, y-3), (x+150, y+23), BLACK, -1)
        cv.putText(frame, f'Dis: {round(distance,2)} inch',
                   (x+5, y+13), FONTS, 0.48, GREEN, 2)
        cv.imwrite("result.jpg", frame)

    return {'data': final_response}

# frame = cv.imread('test_image/test.png')
# output = distance(frame, 1)

# print(output)
