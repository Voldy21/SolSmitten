import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import ss_db as db

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


def listItemsInBucket():
    bucket_name = 'solsmitten-bucket'
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')

    for bucket in s3_resource.buckets.all():
        print(bucket.name)

    for file in my_bucket.objects.all():
        params = {'Bucket': bucket_name, 'Key': file.key}
        url = s3_client.generate_presigned_url('get_object', params)
        print(url)


def getItem(itemName):
    bucket_name = 'solsmitten-bucket'
    my_bucket = s3_resource.Bucket(bucket_name)
    s3_client = boto3.client('s3')
    params = {'Bucket': bucket_name, 'Key': itemName}
    url = s3_client.generate_presigned_url('get_object', params)
    print(url)

# Upload a new file


def uploadFileToS3(fileName):
    bucket_name = 'solsmitten-bucket'
    s3_client = boto3.client('s3')
    data = open(fileName, 'rb')
    s3_client.put_object(Key=fileName, Body=data, Bucket=bucket_name)


getItem("basevase.png")
