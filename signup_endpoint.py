from flask import Flask, jsonify, make_response
import ss_db as db
from flask_restful import Api, Resource, reqparse


signup_args = reqparse.RequestParser()


def initSignup():

    signup_args.add_argument("First name", type=str,
                             help="First name of person", required=True)
    signup_args.add_argument("Last name", type=str,
                             help="Last name of person", required=True)
    signup_args.add_argument("Email", type=str, help="email", required=True)
    signup_args.add_argument("Skin type", type=str,
                             help="type of skin", required=True)
    signup_args.add_argument("Skin feel", type=str,
                             help="Feeling of skin in the morning", required=True)
    signup_args.add_argument("Sensitivity", type=str,
                             help="Skin sensitivity", required=True)
    signup_args.add_argument("Goals", type=str, help="skin goals")
    signup_args.add_argument(
        "Age", type=str, help="Age of the person", required=True)

    signup_args.add_argument(
        "Stress", type=str, help="Rating of stress levels", required=True)
    signup_args.add_argument("Password", type=str,
                             help="Password is required", required=True)
    signup_args.add_argument("Username", type=str,
                             help="Username is required", required=True)


class SignUp(Resource):
    def post(self):
        initSignup()
        args = signup_args.parse_args()
        user_id = db.insert_details(args)
        return {"user": user_id}

    def put(self):
        initSignup()
        args = signup_args.parse_args()
        user_id = db.update_details(args)
        return {"user": user_id}
