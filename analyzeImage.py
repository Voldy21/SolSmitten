# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
from S3Bucket import uploadFileToS3FromStorage
from stopModel import stop_model
from startModel import start_model
import os


def display_image(bucket, photo, response, acneFileName):

    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)
    print(response['CustomLabels'])

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype(os.path.join(
                os.path.dirname((__file__)), "Resources", "arial.ttf"), 50)
            draw.text(
                (left, top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left, top),
                (left + width, top),
                (left + width, top + height),
                (left, top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)
    print(image)
    image.save(os.path.join(
        os.path.dirname((__file__)), "images", "Tom.jpg"))
    url = uploadFileToS3FromStorage(os.path.join(
        os.path.dirname((__file__)), "images", "Tom.jpg"), acneFileName)
    return url


def show_custom_labels(photo, acneFileName):

    bucket = 'solsmitten-bucket'
    model = 'arn:aws:rekognition:us-east-1:671261739394:project/acneDetection/version/acneDetection.2021-04-18T09.41.55/1618753315574'
    min_confidence = 25

    # Start Model parameters required
    project_arn = 'arn:aws:rekognition:us-east-1:671261739394:project/acneDetection/1618752126590'
    model_arn = 'arn:aws:rekognition:us-east-1:671261739394:project/acneDetection/version/acneDetection.2021-04-18T09.41.55/1618753315574'
    min_inference_units = 1
    version_name = 'acneDetection.2021-04-18T09.41.55'

    start_model(project_arn, model_arn, version_name, min_inference_units)

    client = boto3.client('rekognition')

    # Call DetectCustomLabels
    print(photo)
    response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                           MinConfidence=min_confidence,
                                           ProjectVersionArn=model)

    display_image(bucket, photo, response, acneFileName)

    stop_model(model_arn)
    return len(response['CustomLabels'])
