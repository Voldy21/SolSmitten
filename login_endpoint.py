from flask import Flask, jsonify, make_response
import ss_db as db
from flask_restful import Api, Resource, reqparse

login_args = reqparse.RequestParser()


def initLogin():
    login_args.add_argument("username", type=str,
                            help="username required", required=True)
    login_args.add_argument("password", type=str,
                            help="Password Required", required=True)


# Login endpoint
class Login(Resource):
    def get(self):
        return "Hello"

    def post(self):
        initLogin()
        args = login_args.parse_args()
        result = db.login(args)
        if not result:  # if error
            response_body = {
                "message": "Error, Login not found",
            }
            res = make_response(jsonify(response_body), 404)
            return res
        else:  # else return data
            # remove password before sending to user
            result[0].pop("password")
            response_body = {
                "user": result[0]
            }
            res = make_response(jsonify(response_body), 200)
            return res
