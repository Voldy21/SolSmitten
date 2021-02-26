from flask import Flask, jsonify, make_response
import ss_db as db
from flask_restful import Api, Resource, reqparse

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
    signup_args.add_argument("username", type=str,
                             help="Username is required", required=True)


class SignUp(Resource):
    def post(self):
        initSignup()
        args = signup_args.parse_args()
        db.insert_details(args)
        return {"data": args}
