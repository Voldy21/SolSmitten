from flask import Flask, jsonify, make_response, request
import ss_db as db
import os
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete
from s3_functions import UploadImage
from s3_functions import list_files, download_file, upload_file
from werkzeug.utils import secure_filename
from S3Bucket import uploadFileToS3
from wrinkleDetection import wrinkleDetection

BUCKET = "elasticbeanstalk-us-east-1-671261739394"


application = Flask(__name__)
UPLOAD_FOLDER = '/images'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(application)
CORS(application)

api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup")
api.add_resource(Delete, "/delete/<string:name>")


@application.route("/")
def hello():
    details = db.get_details()
    string = {
        "info": details
    }
    return string


@application.route('/uploader', methods=['POST'])
def upload_file_route():
    if request.method == 'POST':
        if request.files:
            f = request.files['file']
            url = uploadFileToS3(f, f.filename)
            x = wrinkleDetection(url, fileName)
            urlSplit = url.split(".")
            uploadFileToS3(x, f'{urlSplit[0]}-wd.{urlSplit[1]}')
            return 'file uploaded successfully'
        return "failed"


api.add_resource(UploadImage, "/upload")


if __name__ == "__main__":
    application.run(port=5000, debug=True)
