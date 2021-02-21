from flask import Flask, jsonify, make_response
import ss_db as db
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

application = Flask(__name__)
api = Api(application)
CORS(application)

signup_args = reqparse.RequestParser()


def initSignup():

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


def initLogin():
    signup_args.add_argument("email", type=str,
                             help="Email Required", required=True)
    signup_args.add_argument("password", type=str,
                             help="Password Required", required=True)


# Signup endpoint
class SignUp(Resource):
    def post(self):
        initSignup()
        args = signup_args.parse_args()
        db.insert_details(args)
        return {"data": args}


# Login endpoint


class Login(Resource):
    def get(self):
        response_body = {
            "message": "Testing",
        }

        res = make_response(jsonify(response_body), 200)
        return res

    def post(self):
        initLogin()
        args = signup_args.parse_args()
        result = db.login(args)
        if not result:  # if error
            response_body = {
                "message": "Error, Login not found",
            }
            res = make_response(jsonify(response_body), 404)
            return res
        else:  # else return data
            result[0].pop("userPassword")
            response_body = {
                "user": result[0]
            }
            res = make_response(jsonify(response_body), 200)
            return res


class Delete(Resource):
    def delete(self, name):
        response = db.delete_user_profile(name)
        return {"response": response}


api.add_resource(Login, "/login")
api.add_resource(SignUp, "/signup/")
api.add_resource(Delete, "/delete/<string:name>")


@application.route("/")
def hello():
    details = db.get_details()
    print(details[0])
    string = ""
    for i in range(len(details[0])):
        string += "".join(str(details[0][i]))
        string += "<br>"
    return string


@application.route("/")
def ping():
    return "ping"


if __name__ == "__main__":
    application.run(port=5000, debug=True)
