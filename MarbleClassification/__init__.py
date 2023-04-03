import logging
import azure.functions as func
import os
import numpy as np
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Get the subscription key and endpoint from environment variables
subscription_key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# Create a Computer Vision client object
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
# Get the URL of the uploaded blob from its properties
    remote_image_url = myblob.uri

    # Call the image analysis API with the blob URL and the desired visual features
    # In this case, we only use the Objects feature to detect the marbles
    image_analysis = computervision_client.analyze_image(remote_image_url, visual_features=[VisualFeatureTypes.objects])

    # Print the results of the analysis in the console
    print("The image has the following objects:")
    for object in image_analysis.objects:
        print(object.object_property)

    # We assume that the area of a fully uncovered marble is 100 square pixels (this may vary depending on the image)
    marble_area = 100

    # We create three empty lists to store the marbles according to their category
    buried_marbles = []
    partial_marbles = []
    uncovered_marbles = []

    # We loop through the detected objects and calculate their area using Numpy
    for object in image_analysis.objects:
        # We get the coordinates of the rectangle that surrounds the object
        x1 = object.rectangle.x
        y1 = object.rectangle.y
        x2 = x1 + object.rectangle.w
        y2 = y1 + object.rectangle.h
        
        # We create a Numpy array with the shape of the rectangle and fill it with ones
        rectangle = np.ones((object.rectangle.h, object.rectangle.w))
        
        # We calculate the area of the object by summing the elements of the array
        object_area = np.sum(rectangle)
        
        # We compare the area of the object with the area of a marble and assign it to a category
        if object_area < marble_area / 3: # If the area is less than a third of the area of a marble, it is fully buried
            buried_marbles.append(object.object_property)
        elif object_area < marble_area * 2 / 3: # If the area is between a third and two thirds of the area of a marble, it is partially buried
            partial_marbles.append(object.object_property)
        else: # If the area is greater than two thirds of the area of a marble, it is fully uncovered
            uncovered_marbles.append(object.object_property)

    # We print the number of marbles in each category
    print("There are {} fully buried marbles".format(len(buried_marbles)))
    print("There are {} partially buried marbles".format(len(partial_marbles)))
    print("There are {} fully uncovered marbles".format(len(uncovered_marbles)))
    
    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )
