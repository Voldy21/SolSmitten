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
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
        target = os.path.join(APP_ROOT,'images/')
        # print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        try:
            file = request.files['file']
            # ASK Jonah for clarification on upload_folder
            destination = '/'.join([target,f.filename])
            file.save(destination)
            upload_file(f"{destination}", BUCKET)
            
            # RUN MODEL
            model.save('model_weights.pth')
            predictions = model.predict(destination)
            labels, boxes, scores = predictions

            print(labels) 
            print(boxes)
            print(scores)
            return {"response", "Success!"}
        except:
            return {"response", "Failed"}


api.add_resource(Upload, "/upload")


if __name__ == "__main__":
    application.run(port=5000, debug=True)
