import cv2
import numpy as np
from urllib.request import urlopen
import os


def wrinkleDetection(imgLocation, fileName):

    def resize(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    lefteye_cascade = cv2.CascadeClassifier(
        "Resources\haarcascade_lefteye_2splits.xml")
    righteye_cascade = cv2.CascadeClassifier(
        "Resources\haarcascade_righteye_2splits.xml")
    face_cascade = cv2.CascadeClassifier(
        "Resources/haarcascade_frontalface_default.xml")
    # eye_cascade = cv2.CascadeClassifier("Resources/haarcascade_eye.xml")
    # nose_cascade = cv2.CascadeClassifier("Resources/Nariz.xml")
    # smile_cascade = cv2.CascadeClassifier("Resources/haarcascade_smile.xml")
    req = urlopen(imgLocation)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    while img.shape[0] > 400:
        img = resize(img, 50)
    while img.shape[0] < 200:
        img = resize(img, 110)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray_img, scaleFactor=1.05, minNeighbors=10)

    for x, y, w, h in faces:
        cropped_img = img[y:y + h, x:x + w]
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        # detect eyes
        lefteye = lefteye_cascade.detectMultiScale(
            cropped_img, scaleFactor=1.05, minNeighbors=10)
        righteye = righteye_cascade.detectMultiScale(
            cropped_img, scaleFactor=1.05, minNeighbors=10)

        # for x, y, w, h in lefteye:
        #     cv2.rectangle(cropped_img, (x, y), (x+w, y+h), (0, 255, 0), 1)
        # for x, y, w, h in righteye:
        #     cv2.rectangle(cropped_img, (x, y), (x+w, y+h), (0, 255, 0), 1)

        # # location of eyes
        if len(lefteye) > 1 and lefteye[0][0] < lefteye[1][0]:
            lefteye[0] = lefteye[1]
        [x1, y1, w1, h1] = lefteye[0]
        [x2, y2, w2, h2] = righteye[0]
        # cv2.rectangle(cropped_img, (x1, y1),
        #               (x1+w1, y1+h1), (0, 255, 0), 1)
        # cv2.rectangle(cropped_img, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 1)
        # cv2.imshow("test", cropped_img)
        # cv2.waitKey(0)

        # corner of the left eye
        corner_left_eye = cropped_img[y1 + h1 //
                                      2:y1 + h1, x1 + w1:x1 + w1 + 12]
        corner_left_eye_canny = cv2.Canny(corner_left_eye, 140, 140)
        corner_left_eye_canny = cv2.cvtColor(
            corner_left_eye_canny, cv2.COLOR_GRAY2BGR)
        left_corner = cv2.bitwise_or(corner_left_eye_canny, corner_left_eye)
        cropped_img[y1 + h1 // 2:y1 + h1, x1 + w1:x1 + w1 + 12] = left_corner

        # corner of the right eye
        corner_right_eye = cropped_img[y2 + h2 // 2:y2 + h2, x2 - 12:x2]
        corner_right_eye_canny = cv2.Canny(corner_right_eye, 140, 140)
        corner_right_eye_canny = cv2.cvtColor(
            corner_right_eye_canny, cv2.COLOR_GRAY2BGR)
        right_corner = cv2.bitwise_or(corner_right_eye_canny, corner_right_eye)
        cropped_img[y2 + h2 // 2:y2 + h2, x2 - 12:x2] = right_corner
        # # find left and right eyes
        leftX = min(x1, x2)  # top left corner of left eye
        rightX = max(x1, x2)  # top left corner of right eye
        maxY = min(y1, y2)  # y coordinate of higher eye

        # isolate under the left eye
        under_left_eye = cropped_img[y1 + h1 - 6:y1 + h1 + 10, x1:x1 + w1]
        under_left_eye_canny = cv2.Canny(under_left_eye, 140, 140)
        under_left_eye_canny = cv2.cvtColor(
            under_left_eye_canny, cv2.COLOR_GRAY2BGR)
        left = cv2.bitwise_or(under_left_eye_canny, under_left_eye)
        cropped_img[y1 + h1 - 6:y1 + h1 + 10, x1:x1 + w1] = left

        # isolate under the right eye
        under_right_eye = cropped_img[y2 + h2 - 5:y2 + h2 + 10, x2:x2 + w2]
        under_right_eye_canny = cv2.Canny(under_right_eye, 140, 140)
        under_right_eye_canny = cv2.cvtColor(
            under_right_eye_canny, cv2.COLOR_GRAY2BGR)
        right = cv2.bitwise_or(under_right_eye_canny, under_right_eye)
        cropped_img[y2 + h2 - 5:y2 + h2 + 10, x2:x2 + w2] = right

        # # isolate forehead
        forehead = cropped_img[10:maxY, leftX:rightX + w2]
        forehead_edges = cv2.Canny(forehead, 100, 100)
        forehead_edges = cv2.cvtColor(
            forehead_edges, cv2.COLOR_GRAY2BGR)

        img1_bg = cv2.bitwise_or(forehead_edges, forehead)
        cropped_img[10:maxY, leftX:rightX + w2] = img1_bg
        img[y:y + h, x:x + w] = cropped_img
        directory = os.path.join(os.path.dirname((__file__)), "images")
        os.chdir(directory)
        cv2.imwrite(fileName, img)
        return np.count_nonzero(forehead_edges)
