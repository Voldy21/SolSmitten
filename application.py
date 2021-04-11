from flask import Flask, jsonify, make_response, request
import ss_db as db
import os
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete
from home import Base
from S3Bucket import list_files, download_file, upload_file, UploadImage, uploadFileToS3FromStorage
from werkzeug.utils import secure_filename
from S3Bucket import uploadFileToS3
from wrinkleDetection import wrinkleDetection
import datetime

BUCKET = "elasticbeanstalk-us-east-1-671261739394"


application = Flask(__name__)
UPLOAD_FOLDER = '/images'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(application)
CORS(application)

api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")
api.add_resource(Delete, "/delete/<string:name>")
api.add_resource(UploadImage, "/upload")
api.add_resource(Base, "/home")


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


# @application.route("/<username>")
# def find(username):
#     details = db.getUser_ID(username)
#     return {"user_id": details['primary_key']}


@application.route('/uploader', methods=['GET', 'POST'])
def upload_file_route():
    if request.method == 'POST':
        if request.files:
            "46-wd-4-10-21 1-20-21.jpg"
            # try:
            timeStamp = str(datetime.datetime.now()).split('.')[
                0].replace(":", "-")
            f = request.files['file']
            urlSplit = f.filename.split(".")
            user_id = urlSplit[0]
            fileName = f'{user_id}-{timeStamp}.{urlSplit[1]}'
            # save original image to s3 bucket
            originalURL = uploadFileToS3(f, fileName)
            # split name wrinkleDetection filename
            wrinkleDetectionName = f'{user_id}-wd-{timeStamp}.{urlSplit[1]}'
            # send image through wrinkle detection
            wrinkleScore = wrinkleDetection(
                originalURL, wrinkleDetectionName)
            if wrinkleScore == 0:
                return "failure"
            print(wrinkleScore)

            # upload processed image to s3 bucket
            wrinkleURL = uploadFileToS3FromStorage(os.path.join(
                os.path.dirname((__file__)), "images", wrinkleDetectionName), wrinkleDetectionName)
            db.insert_image_details(
                wrinkleURL, originalURL, wrinkleScore, user_id)
            return "success"
            # except:
            #     return "failed"
            # return str(x)
        return "failed"


if __name__ == "__main__":
    application.run(port=5000, debug=True)
