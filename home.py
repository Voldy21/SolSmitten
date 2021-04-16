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
        print(args)
        result = db.getData(args)
        return {"message": result}

    def get(self):
        download_file("50-020bb153-c4c6-4588-9d46-1b57e836532c.jpg")
        return 0
