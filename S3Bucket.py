import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import ss_db as db

from flask import Flask, jsonify, make_response, request
import boto3
import os
import werkzeug
#from flask_restful import Resource, reqparse, Api

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
bucket_name = 'solsmitten-bucket'

# s3 = boto3.client(
#     's3',
#     aws_access_key_id=ACCESS_KEY_ID,
#     aws_secret_access_key=ACCESS_SECRET_KEY)
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket(bucket_name)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def listItemsInBucket():
    bucket_name = 'solsmitten-bucket'
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')

    # for bucket in s3_resource.buckets.all():
    #     print(bucket.name)

    # for file in my_bucket.objects.all():
    #     params = {'Bucket': bucket_name, 'Key': file.key}
    #     url = s3_client.generate_presigned_url('get_object', params)
    #     print(url)


def getItem(itemName):
    bucket_name = 'solsmitten-bucket'
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')
    params = {'Bucket': bucket_name, 'Key': itemName}
    url = s3_client.generate_presigned_url('get_object', params)
    print(url)


# Upload a new file
def uploadFileToS3(img, fileName, folder_path):
    bucket_name = 'solsmitten-bucket'
    s3 = boto3.resource('s3')
    params = {'Bucket': bucket_name, 'Key': fileName}
    # for folder in s3_client.list_objects(Bucket=bucket_name):
    #     if folder == folder_path:
    s3.Bucket(bucket_name).upload_file(img, '%s/%s' %(folder_path, img))
    url = s3_client.generate_presigned_url('get_object', params)
    print("image in bucket")

    return url

# Upload a new file from disk


def uploadFileToS3FromStorage(location, fileName):
    bucket_name = 'solsmitten-bucket'
    params = {'Bucket': bucket_name, 'Key': fileName}
    s3_client = boto3.client('s3')
    data = open(fileName, 'rb')
    s3_client.put_object(Key=fileName, Body=data, Bucket=bucket_name)
    url = s3_client.generate_presigned_url('get_object', params)
    return url


# class UploadImage(Resource):
#     def post(self):
#         parse = reqparse.RequestParser()
#         parse.add_argument(
#             'file', type=werkzeug.datastructures.FileStorage, location='/images')
#         parse.add_argument('user_id', type=int)
#         args = parse.parse_args()
#         print(args)
#         image_file = args['file']
#         if image_file:
#             image_file.save("your_file_name.jpg")
#         return "hello"


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return response


def download_file(file_name):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.client('s3')
    output = f"downloads/{file_name}"
    s3.download_file('solsmitten-bucket', file_name, "images/test.jpg")
    return "test.jpg"


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents

def create_user_folder(user_name):
    folder_name = user_name + "_images"
  
    s3_client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))

    return folder_name


