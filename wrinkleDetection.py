import cv2
import numpy as np
from urllib.request import urlopen
import os
from S3Bucket import uploadFileToS3FromStorage


def fixImage(imgLocation, fileName):
    def resize(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    # Read the image
    img = cv2.imread(imgLocation)
    i = 0
    while(np.logical_and(img is None, i < 4)):
        img = cv2.imread(os.path.join("images", imgLocation))
        i += 1

    # call the haarcascade for finding a face
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # readjust the image to be a certain size
    while img.shape[0] > 500:
        img = resize(img, 80)
    while img.shape[0] < 300:
        img = resize(img, 110)

    # Try to find the face and rotate if cannot find
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if len(gray_img) != 0:
        faces = face_cascade.detectMultiScale(
            gray_img, scaleFactor=1.1, minNeighbors=10)
        i = 0
        while(np.logical_and(len(faces) == 0, i < 4)):
            img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray_img, scaleFactor=1.1, minNeighbors=10)
            i += 1

        imagePath = os.path.join(os.path.dirname(
            __file__), "images", fileName)
        cv2.imwrite(imagePath, img)
        imgURL = uploadFileToS3FromStorage(imagePath, fileName)
        if os.path.exists(imagePath):
            os.remove(imagePath)
        return imgURL
    else:
        print("no image")
        return "failure"


def wrinkleDetection(imgLocation, fileName):
    # Call the haarcascades in order to locate features of the face
    lefteye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_lefteye_2splits.xml")
    righteye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_righteye_2splits.xml")
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Open the image
    req = urlopen(imgLocation)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # If a face could not be found then return an error message
    if len(gray_img) != 0:
        faces = face_cascade.detectMultiScale(
            gray_img, scaleFactor=1.1, minNeighbors=10)
        i = 0
    else:
        return "failure"

    for x, y, w, h in faces:
        # Crop the original image
        cropped_img = img[y:y + h, x:x + w]
        # Get the grayscaled version of the cropped image
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        # detect eyes
        lefteye = lefteye_cascade.detectMultiScale(
            cropped_img, scaleFactor=1.1, minNeighbors=10)
        righteye = righteye_cascade.detectMultiScale(
            cropped_img, scaleFactor=1.1, minNeighbors=10)

        # location of eyes
        if len(lefteye) > 1 and lefteye[0][0] < lefteye[1][0]:
            lefteye[0] = lefteye[1]
        [x1, y1, w1, h1] = lefteye[0]
        [x2, y2, w2, h2] = righteye[0]

        # corner of the left eye
        corner_left_eye = cropped_img[y1 + h1 //
                                      2:y1 + h1, x1 + w1:x1 + w1 + 10]
        corner_left_eye_canny = cv2.Canny(corner_left_eye, 140, 140)
        corner_left_eye_canny = cv2.cvtColor(
            corner_left_eye_canny, cv2.COLOR_GRAY2BGR)
        left_corner = cv2.bitwise_or(corner_left_eye_canny, corner_left_eye)
        cropped_img[y1 + h1 // 2:y1 + h1, x1 + w1:x1 + w1 + 10] = left_corner

        # corner of the right eye
        corner_right_eye = cropped_img[y2 + h2 // 2:y2 + h2, x2 - 10:x2]
        corner_right_eye_canny = cv2.Canny(corner_right_eye, 140, 140)
        corner_right_eye_canny = cv2.cvtColor(
            corner_right_eye_canny, cv2.COLOR_GRAY2BGR)
        right_corner = cv2.bitwise_or(corner_right_eye_canny, corner_right_eye)
        cropped_img[y2 + h2 // 2:y2 + h2, x2 - 10:x2] = right_corner
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

        # impose the canny image over the original image
        img1_bg = cv2.bitwise_or(forehead_edges, forehead)
        cropped_img[10:maxY, leftX:rightX + w2] = img1_bg

        # impose the cropped image onto the original image
        img[y:y + h, x:x + w] = cropped_img

        # Save the wrinkleDetection image in "/images"
        directory = os.path.join(os.path.dirname((__file__)), "images")
        os.chdir(directory)
        cv2.imwrite(fileName, img)

        # Calculate score for the user
        score = np.count_nonzero(under_left_eye_canny)
        adjusted_score = 10 + (score - 0) * (0 - 10) / (600 - 0)
        return int(adjusted_score)
