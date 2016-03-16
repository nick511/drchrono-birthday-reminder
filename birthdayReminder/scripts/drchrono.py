
import urllib.parse
import requests

BASE_URL = 'https://drchrono.com'
AUTHORIZE_URL = BASE_URL + '/o/authorize/'

ENDPOINT_TOKEN = '/o/token/'
ENDPOINT_PATIENTS_SUMMARY = '/api/patients_summary'




class DrChronoClient(object):

  access_token = None

  def __init__(self, client_id, client_secret, redirect_uri):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri


  def get_authorize_url(self):
    authSettings = {'response_type': 'code',
                    'client_id': self.client_id,
                    'redirect_uri': self.redirect_uri,
                    }

    params = urllib.parse.urlencode(authSettings)

    return AUTHORIZE_URL + '?' + params


  def get_patients_summary(self, token):

    response = requests.get(BASE_URL + ENDPOINT_PATIENTS_SUMMARY, headers=self.get_auth_headers(token))

    response.raise_for_status()
    data = response.json()
    print(data)


  def get_auth_headers(self, token):
    access_token = token['access_token']
    header_authorization = 'Bearer %s' % access_token

    return {
      'Authorization': header_authorization,
    }


  def get_token(self, code):

    # Token exchange
    response = requests.post(BASE_URL + ENDPOINT_TOKEN, data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': self.redirect_uri,
        'client_id': self.client_id,
        'client_secret': self.client_secret,
    })

    response.raise_for_status()
    data = response.json()

    return data
