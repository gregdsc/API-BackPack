# Imports the Google Cloud client library
from google.oauth2 import service_account

# local windows
#credentials = service_account.Credentials.from_service_account_file(
 #   r'C:\Users\Alexandre\PycharmProjects\Backpack-api\project.json')


# dev / prod
credentials = service_account.Credentials. from_service_account_file(r'project.json')

# clients = vision.ImageAnnotatorClient(credentials=credentials)


def detect_properties_uri(uri):
    """Detects image properties in the file located in Google Cloud Storage or
    on the Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
    print(response)
