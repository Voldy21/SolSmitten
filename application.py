from flask import Flask, jsonify, make_response, request
import ss_db as db
import os
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete
from home import Base, BaseData
from S3Bucket import list_files, download_file, upload_file, uploadFileToS3FromStorage
from werkzeug.utils import secure_filename
from wrinkleDetection import wrinkleDetection, fixImage
from startModel import start_model
from stopModel import stop_model
from analyzeImage import show_custom_labels
import datetime
import uuid


BUCKET = "elasticbeanstalk-us-east-1-671261739394"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

application = Flask(__name__)
UPLOAD_FOLDER = '/images'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(application)
CORS(application)

api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")
api.add_resource(Delete, "/delete/<string:name>")
# api.add_resource(UploadImage, "/upload")
api.add_resource(Base, "/home")
api.add_resource(BaseData, "/home/<user_id>")


@application.route("/")
def hello():
    details = db.get_details()
    string = {
        "info": details
    }
    return string


@application.route("/images")
def Images():
    details = db.get_Image_details()
    string = {
        "info": details
    }
    return string


@application.route('/uploader', methods=['GET', 'POST'])
def upload_file_route():
    if request.method == 'POST':
        if request.files:
            # try:
            unique_id = uuid.uuid4()
            f = request.files['file']
            urlSplit = f.filename.split(".")
            user_id = urlSplit[0]
            fileName = f'{user_id}-{unique_id}.{urlSplit[1]}'
            # Path to image on disc
            imgPath = os.path.join(
                os.path.dirname((__file__)), "images", fileName)
            # Save image to disc
            f.save(imgPath)
            # Rotate and resize image along with uploading image to S3 bucket and get URL back
            originalURL = fixImage(imgPath, fileName)
            # Assign file names for wrinkle detection and acne detection images
            wrinkleDetectionName = f'{user_id}-wd-{unique_id}.{urlSplit[1]}'
            acneDetectionName = f'{user_id}-ad-{unique_id}.{urlSplit[1]}'

            # # send image through wrinkle detection
            wrinkleScore = wrinkleDetection(
                originalURL, wrinkleDetectionName)
            # upload processed image to s3 bucket
            wrinkleURL = uploadFileToS3FromStorage(os.path.join(
                os.path.dirname((__file__)), "images", wrinkleDetectionName), wrinkleDetectionName)
            # Acne detection
            # acneURL = show_custom_labels(fileName, acneDetectionName)
            # Insert Data to database
            db.insert_image_details(
                wrinkleURL, originalURL, wrinkleScore, user_id)
            # Remove images that are currently in image folder
            if os.path.exists(wrinkleDetectionName):
                os.remove(wrinkleDetectionName)
            return {
                "wrinkleURL": wrinkleURL,
                "originalURL": originalURL,
                "WrinkleScore": wrinkleScore,
                "user_id": user_id
            }
            # except:
            #     return "failed"
            # return str(x)
        return {"message", "failure"}


if __name__ == "__main__":
    application.run(port=5000, debug=True)
