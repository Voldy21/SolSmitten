import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import ss_db as db

from flask import Flask, jsonify, make_response, request
import os
import werkzeug
from config import S3_KEY, S3_SECRET, AWS_SESSION_TOKEN
#from flask_restful import Resource, reqparse, Api


def getBucketName():
    return 'solsmitten2'


bucket_name = getBucketName()


s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET,
    region_name="us-east-2"

)
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket(bucket_name)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def listItemsInBucket():
    bucket_name = getBucketName()
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')


def getItem(itemName):
    bucket_name = getBucketName()
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')
    params = {'Bucket': bucket_name, 'Key': itemName}
    url = s3_client.generate_presigned_url('get_object', params)
    print(url)


def upload_file_to_s3(imagePath, filename):
    bucket_name = "solsmitten2"
    file = open(imagePath, 'rb')
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
        )
        params = {'Bucket': bucket_name, 'Key': filename}
        url = s3.generate_presigned_url('get_object', params, ExpiresIn=604800 )
        if os.path.exists(imagePath):
            os.remove(imagePath)
        return url

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        return {"message": "failure",
                "error": str(e),
                }


def uploadFileToS3FromStorage(location, fileName):
    bucket_name = getBucketName()
    params = {'Bucket': bucket_name, 'Key': fileName}
    s3_client = boto3.client('s3')
    data = open(location, 'rb')
    s3_client.put_object(Key=fileName, Body=data, Bucket=bucket_name)
    url = s3_client.generate_presigned_url('get_object', params)
    print(url)
    return url


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
    s3.download_file('solsmitten', file_name, "images/test.jpg")
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

    s3_client.put_object(Bucket=bucket_name, Key=(folder_name + '/'))

    return folder_name
