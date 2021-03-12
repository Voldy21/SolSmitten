import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import ss_db as db

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
bucket_name = 'solsmitten'

# s3 = boto3.client(
#     's3', 
#     aws_access_key_id=ACCESS_KEY_ID,
#     aws_secret_access_key=ACCESS_SECRET_KEY)
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket(bucket_name)

# for bucket in s3_resource.buckets.all():
#     print(bucket.name)

for file in my_bucket.objects.all():
    params = {'Bucket': bucket_name, 'Key': file.key}
    url = s3_client.generate_presigned_url('get_object', params)
    db.add_image_url(url)
    print ("URL was loaded into Database!")
    print(url)

# Upload a new file
# data = open('basevase.png', 'rb')
# s3.Bucket('solsmitten').put_object(Key='basevase.png', Body=data)