from flask import Flask, jsonify, make_response, request
import boto3
import os
import werkzeug
from flask_restful import Resource, reqparse, Api

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class UploadImage(Resource):
    def post(self):

        parse = reqparse.RequestParser()
        parse.add_argument(
            'file', type=werkzeug.datastructures.FileStorage, location='/images')
        args = parse.parse_args()
        print(args)
        image_file = args['file']
        if image_file:
            image_file.save("your_file_name.jpg")


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response


def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = f"downloads/{file_name}"
    s3.Bucket(bucket).download_file(file_name, output)

    return output


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents
