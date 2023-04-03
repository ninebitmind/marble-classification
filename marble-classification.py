import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Get the subscription key and endpoint from environment variables
subscription_key = os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["COMPUTER_VISION_ENDPOINT"]

# Create a Computer Vision client object
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Get the URL of the uploaded blob from its properties
image_url = os.environ["BLOB_URL"]

detect_objects_results = computervision_client.detect_objects(image_url)

marble_count = 0

for object in detect_objects_results.objects:
    if object.object_property == 'marble':
        marble_count += 1

print('Number of marbles detected:', marble_count)