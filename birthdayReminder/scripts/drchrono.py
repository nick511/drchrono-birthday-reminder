
import urllib.parse
import requests

BASE_URL = 'https://drchrono.com'
AUTHORIZE_URL = BASE_URL + '/o/authorize/'

ENDPOINT_TOKEN = BASE_URL + '/o/token/'

ENDPOINT_API = BASE_URL + '/api'
ENDPOINT_CURRENT_USER = ENDPOINT_API + '/users/current'
ENDPOINT_PATIENTS = ENDPOINT_API + '/patients'
ENDPOINT_PATIENTS_SUMMARY = ENDPOINT_API + '/patients_summary'


class DrChronoClient(object):


  def __init__(self, client_id, client_secret, redirect_uri):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri


  # Step 1: Redirect to drchrono
  # Step 2: Provider authorization
  def get_authorize_url(self):
    authSettings = {'response_type': 'code',
                    'client_id': self.client_id,
                    'redirect_uri': self.redirect_uri,
                    }

    params = urllib.parse.urlencode(authSettings)

    return AUTHORIZE_URL + '?' + params


  # Step 3: Token exchange
  def get_token(self, code):

    response = requests.post(ENDPOINT_TOKEN, data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': self.redirect_uri,
        'client_id': self.client_id,
        'client_secret': self.client_secret,
    })

    response.raise_for_status()
    data = response.json()

    return data


  def refresh_token(self, refresh_token):
    response = requests.post(ENDPOINT_TOKEN, data={
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': self.client_id,
        'client_secret': self.client_secret,
    })

    response.raise_for_status()
    data = response.json()

    return data


  # /users/current
  def get_current_user(self, access_token):

    headers = self.get_auth_headers(access_token)
    response = requests.get(ENDPOINT_CURRENT_USER, headers=headers)
    response.raise_for_status()
    data = response.json()

    return data


  # /api/patients
  def get_patients(self, access_token, filter=None):

    api_url = ENDPOINT_PATIENTS

    if filter:
      params = urllib.parse.urlencode(filter)
      api_url += '?' + urllib.parse.unquote_plus(params)

    patients = self.get_paged_data(access_token, api_url)

    return patients


  # /api/patients_summary
  def get_patients_summary(self, access_token):

    patients = self.get_paged_data(access_token, ENDPOINT_PATIENTS_SUMMARY)

    return patients


  def get_paged_data(self, access_token, data_url):

    data = []
    headers = self.get_auth_headers(access_token)

    while data_url:
      response = requests.get(data_url, headers=headers)
      response.raise_for_status()
      json = response.json()
      data.extend(json['results'])

      data_url = json['next'] # A JSON null on the last page

    return data


  # headers - Authorization
  def get_auth_headers(self, access_token):
    header_authorization = 'Bearer %s' % access_token

    return {
      'Authorization': header_authorization,
    }



