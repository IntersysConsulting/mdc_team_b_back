import json
import requests
import tempfile
from werkzeug.datastructures import FileStorage


def upload_image(remote_image,
                 title='',
                 description='',
                 auth='cb644a31670bc8e'):
    ''' This function will upload image to imgur

        Arguments:
        remote_image:   The incoming image as a FileStorage
        title:          A name for the image (not required)
        description:    A descrtiption for the image (not required) 
        aut:            OAuth token for imgur, the default value will work 

        Return:
        Json with status, success and link of the image. All the info comes from
        imgur API   
    '''

    ret_val = None

    if remote_image is None:
        ret_val = {'status': '400', 'success': False, 'link': ''}
    else:
        temporary_directory = tempfile.TemporaryDirectory()
        path = "{}\\{}".format(temporary_directory.name, remote_image.filename)
        remote_image.save(path)

        with open(path, 'rb') as fp:
            image = fp.read()

        payload = {'image': image, 'title': title, 'description': description}

        headers = {'Authorization': 'Client-ID {}'.format(auth)}
        response = requests.post(url='https://api.imgur.com/3/image',
                                 headers=headers,
                                 data=payload).json()

        ret_val = {
            'status': response['status'],
            'success': response['success'],
            'link': response['data']['link']
        }

        temporary_directory.cleanup()

    return ret_val
