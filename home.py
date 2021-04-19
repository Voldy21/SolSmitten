from flask import Flask, jsonify, make_response
import ss_db as db
from flask_restful import Api, Resource, reqparse
from S3Bucket import download_file

login_args = reqparse.RequestParser()

home_args = reqparse.RequestParser()


# Login endpoint
class Base(Resource):
    def post(self):
        home_args.add_argument("user_id", type=int)
        args = home_args.parse_args()
        result = db.getData(args)
        name = db.getName(args)
        return {
            "message": result,
            "name": name}

    def put(self):
        home_args.add_argument("user_id", type=int)
        args = home_args.parse_args()
        name = db.getName(args)
        return {"data": name}


class BaseData(Resource):
    def get(self, user_id):
        try:
            name = db.getName({"user_id": user_id})
            return {"data": name}
        except:
            return {"message": "failed"}
