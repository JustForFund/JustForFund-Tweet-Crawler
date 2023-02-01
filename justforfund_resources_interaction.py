import requests
import os

BASE_URL = 'https://justfor.fund/api/v1'
API_KEY = os.environ['JUSTFORFUND_RESOURCE_API_KEY']
API_SECRET = os.environ['JUSTFORFUND_RESOURCE_SECRET_KEY']
HEADERS = {'API-KEY': API_KEY, 'API-SECRET': API_SECRET}

        
def upload_resource(resource_id, resource_dict):
    url = "{}/upload_resource".format(BASE_URL)
    data = {
        'resource_id': resource_id,
        'resource_dict': resource_dict
    }
    r = requests.post(url, json=data, headers=HEADERS)
    print(r)
    return r