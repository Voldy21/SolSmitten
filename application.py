from flask import Flask, jsonify, make_response, request
import ss_db as db
import os
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete
from home import Base, BaseData
from S3Bucket import list_files, download_file, upload_file, uploadFileToS3FromStorage, upload_file_to_s3
from werkzeug.utils import secure_filename
from wrinkleDetection import wrinkleDetection, fixImage
from startModel import start_model
from stopModel import stop_model
from analyzeImage import show_custom_labels
import datetime
import uuid
from config import S3_KEY, S3_SECRET


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


# @application.route("/")
# def hello():
#     # details = db.get_details()
#     # string = {
#     #     "info": details
#     # }
#     # return string
#     return "homepage"


# @application.route("/images")
# def Images():
#     # details = db.get_Image_details()
#     # string = {
#     #     "info": details
#     # }
#     # return string
#     pass


# @application.route('/uploaders', methods=['GET', 'POST'])
# def test_routing():
#     if request.method == 'POST':
#         if request.files:
#             f = request.files["file"]
#             x = upload_file_to_s3(f, f.filename)
#             print(f.filename)
#             return x



# main uploading path
@application.route('/uploader', methods=['GET', 'POST'])
def upload_file_route():
    if request.method == 'POST':
        if request.files:
            try:
                unique_id = uuid.uuid4()
                f = request.files['file']
                urlSplit = f.filename.split(".")
                user_id = urlSplit[0]
                fileName = f'{user_id}-{unique_id}.{urlSplit[1]}'

            except:
                return "first part failure"
            # Rotate and resize image along with uploading image to S3 bucket and get URL back
            originalURL = fixImage(f, fileName)
            if isinstance(originalURL, dict):
                return originalURL

            # Assign file names for wrinkle detection and acne detection images
            wrinkleDetectionName = f'{user_id}-wd-{unique_id}.{urlSplit[1]}'
            # acneDetectionName = f'{user_id}-ad-{unique_id}.{urlSplit[1]}'
            # # send image through wrinkle detection
            wrinkleScore = wrinkleDetection(
                originalURL, wrinkleDetectionName)
            if wrinkleScore is -1:
                return {"message": "failed to get wrinkleScore"}
            # upload processed image to s3 bucket
            wrinkleURL = upload_file_to_s3(os.path.join(
                os.path.dirname((__file__)), "images", wrinkleDetectionName), wrinkleDetectionName)
            if isinstance(wrinkleURL, dict):
                return wrinkleURL
            if wrinkleURL is -1:
                return str(wrinkleURL)

            # Insert Data to database
            x = db.insert_image_details(
                wrinkleURL, originalURL, wrinkleScore, user_id)
            
            if x != "success":
                return x
            # Acne detection
            # show_custom_labels(fileName, acneDetectionName, fileID)
            return {
                "wrinkleURL": wrinkleURL,
                "originalURL": originalURL,
                "WrinkleScore": wrinkleScore,
                "user_id": user_id
            }
        return {"message", "failure"}
    return "goodbye"


if __name__ == "__main__":
    application.run(port=5000, debug=True)
