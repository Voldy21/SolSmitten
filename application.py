from flask import Flask, jsonify, make_response
import ss_db as db
import os
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete
from s3_functions import list_files, download_file, upload_file

BUCKET = "elasticbeanstalk-us-east-1-671261739394"


application = Flask(__name__)
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


class Upload(Resource):
    def post(self):
        try:
            f = request.files['file']
            f.save(os.path.join(UPLOAD_FOLDER, f.filename))
            upload_file(f"uploads/{f.filename}", BUCKET)

            return {"response", "Success!"}
        except:
            return {"response", "Failed"}


api.add_resource(Upload, "/upload")


if __name__ == "__main__":
    application.run(port=5000, debug=True)
