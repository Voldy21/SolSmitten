model.save('model_weights.pth')
# Specify the path to your image
image = utils.read_image('testImages/testImage2.png')
predictions = model.predict(image)

# predictions format: (labels, boxes, scores)
labels, boxes, scores = predictions

print(labels) 

print(boxes)

print(scores)