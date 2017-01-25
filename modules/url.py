import requests
import json
import os

KEY = os.environ['GOOGLEAPI']

def shortUrl(longUrl):
    apiUrl = 'https://www.googleapis.com/urlshortener/v1/url?key=' + KEY
    headers = {'content-type': 'application/json'}
    data = {
        'longUrl' : longUrl
    }
    r = requests.post(apiUrl , data=json.dumps(data) , headers = headers)
    result = r.json()
    return result['id']



def expandUrl(shortUrl):
    r = requests.get('https://www.googleapis.com/urlshortener/v1/url', params={
        'key': KEY,
        'shortUrl': shortUrl
    })

    data = r.json()
    return data['longUrl']

