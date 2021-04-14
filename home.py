from flask import Flask, jsonify, make_response
import ss_db as db
from flask_restful import Api, Resource, reqparse

login_args = reqparse.RequestParser()

home_args = reqparse.RequestParser()


# Login endpoint
class Base(Resource):
    def post(self):
        home_args.add_argument("user_id", type=int)
        args = home_args.parse_args()
        print(args)
        result = db.getData(args)
        return {"message": result}
