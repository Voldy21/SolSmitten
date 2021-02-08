from flask import Flask
import ss_db as db
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

application = Flask(__name__)
api = Api(application)
CORS(application)

signup_args = reqparse.RequestParser()
signup_args.add_argument("firstName", type=str,
                         help="First name of person", required=True)
signup_args.add_argument("lastName", type=str,
                         help="Last name of person", required=True)
signup_args.add_argument("email", type=str, help="email", required=True)
signup_args.add_argument("skinType", type=str,
                         help="type of skin", required=True)
signup_args.add_argument("skinFeel", type=str,
                         help="Feeling of skin in the morning", required=True)
signup_args.add_argument("sensitivity", type=str,
                         help="Skin sensitivity", required=True)
signup_args.add_argument("goals", type=str, help="skin goals")
signup_args.add_argument(
    "age", type=str, help="Age of the person", required=True)

signup_args.add_argument(
    "stress", type=str, help="Rating of stress levels", required=True)
signup_args.add_argument("password", type=str,
                         help="Password is required", required=True)


class SignUp(Resource):
    def post(self):
        args = signup_args.parse_args()
        db.insert_details(args)
        return {"data": args}

    def delete(self, name):
        response = db.delete_user_profile(name)
        return {"response": response}


api.add_resource(SignUp, "/signup/<string:name>")


@application.route("/")
def hello():
    details = db.get_details()
    string = ""
    for i in range(len(details)):
        string += "".join(str(details[i]))
        string += "<br>"
    return string


@application.route("/ping")
def ping():
    return "ping"


if __name__ == "__main__":
    application.run(debug=True)
