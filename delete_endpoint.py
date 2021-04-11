# Delete endpoint
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse
import ss_db as db


class Delete(Resource):
    def delete(self, name):
        response = db.delete_user_profile(name)
        return {"response": response}

    def post(self, name):
        response = db.delete_all_images()
        return response

    # def post(self, name):
    #     response = db.delete_all()
    #     return {"response": response}
