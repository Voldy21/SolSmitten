from flask import Flask, jsonify, make_response
import ss_db as db
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
from signup_endpoint import SignUp
from login_endpoint import Login
from delete_endpoint import Delete

application = Flask(__name__)
api = Api(application)
CORS(application)

api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup/")
api.add_resource(Delete, "/delete/<string:name>")


@application.route("/")
def hello():
    details = db.get_details()
    string = {
        "info": details
    }
    return string


if __name__ == "__main__":
    application.run(port=5000, debug=True)
