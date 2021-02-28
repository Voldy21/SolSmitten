from flask import Flask, jsonify, make_response
import requests # to get image from the web
import shutil # to save image locally


app = Flask(_name_)


def saveImageLocally(image_url):
    filename = image_url.split("/")[-1]
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        return filename
    else:
        print('Image Couldn\'t be retreived')


@app.route('/imagePath/<String:link>',methods=['GET'])
def imageProcessing(link):

    model.save('model_weights.pth')

    # Specify the path to image
    image = saveImageLocally(link)
    predictions = model.predict(image)

    # predictions format: (labels, boxes, scores)
    labels, boxes, scores = predictions

    print(labels) 

    print(boxes)

    print(scores)