# flask_s3_uploads/config.py

import os
S3_BUCKET = "solsmitten"
S3_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.environ.get("SESSION_TOKEN")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000
