# Imports the Google Cloud client library
from google.oauth2 import service_account

# # local windows
# credentials = service_account.Credentials.from_service_account_file(
#     r'C:\Users\Alexandre\PycharmProjects\Backpack-api\project.json')


# dev / prod
from google.protobuf.json_format import MessageToDict

credentials = service_account.Credentials. from_service_account_file(r'project.json')

# clients = vision.ImageAnnotatorClient(credentials=credentials)

#
# from google.cloud import vision
#
# client = vision.ImageAnnotatorClient(credentials=credentials)
# image = vision.types.Image()
# image.source.image_uri = "https://res.cloudinary.com/hpnctvfmr/image/upload/v1568138914/photo-1531874824027-2a0d33bd6338.jpg.jpg"

def detect_web_uri(uri):
    """Detects web annotations in the file located in Google Cloud Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.web_detection(image=image)
    annotations = response.web_detection

    dict = {}

    if annotations.best_guess_labels:
        for label in annotations.best_guess_labels:
            print('\nBest guess label: {}'.format(label.label))
            dict['best guess label'] = label.label

    if annotations.pages_with_matching_images:
        print('\n{} Pages with matching images found:'.format(
            len(annotations.pages_with_matching_images)))

        for page in reversed(annotations.pages_with_matching_images):
            print('\n\tPage url   : {}'.format(page.url))
            dict['page_url'] = page.url

            if page.full_matching_images:
                print('\t{} Full Matches found: '.format(
                       len(page.full_matching_images)))
                #dict['page_full_matching_images'] = page.full_matching_images

                for image in page.full_matching_images:
                    print('\t\tImage url  : {}'.format(image.url))
                    #dict['image_url'] = image.url

            if page.partial_matching_images:
                print('\t{} Partial Matches found: '.format(
                       len(page.partial_matching_images)))
                #dict['partial_matches_found'] = page.partial_matching_images

                for image in reversed(page.partial_matching_images):
                    print('\t\tImage url  : {}'.format(image.url))
                    dict['image_url_2'] = image.url

    if annotations.web_entities:
        print('\n{} Web entities found: '.format(
            len(annotations.web_entities)))

        for entity in reversed(annotations.web_entities):
            print('\n\tScore      : {}'.format(entity.score))
            print(u'\tDescription: {}'.format(entity.description))
            dict['Score'] = entity.score
            dict['Description'] = entity.description

    if annotations.visually_similar_images:
        print('\n{} visually similar images found:\n'.format(
            len(annotations.visually_similar_images)))

        for image in reversed(annotations.visually_similar_images):
            print('\tImage url    : {}'.format(image.url))
            dict['image_similar'] = image.url

    return dict

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

