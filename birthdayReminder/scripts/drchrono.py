
import urllib.parse
import requests

BASE_URL = 'https://drchrono.com'
AUTHORIZE_URL = BASE_URL + '/o/authorize/'

ENDPOINT_TOKEN = '/o/token/'
ENDPOINT_PATIENTS = '/api/patients'
ENDPOINT_PATIENTS_SUMMARY = '/api/patients_summary'


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

    response = requests.post(BASE_URL + ENDPOINT_TOKEN, data={
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': self.redirect_uri,
        'client_id': self.client_id,
        'client_secret': self.client_secret,
    })

    response.raise_for_status()
    data = response.json()

    #TODO: refresh_token()
    #access_token = data['access_token']
    #refresh_token = data['refresh_token']
    #expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

    return data

  # /api/patients
  def get_patients(self, token):

    patients_url = BASE_URL + ENDPOINT_PATIENTS
    patients = self.get_paged_data(token, patients_url)

    return patients

  # /api/patients_summary
  def get_patients_summary(self, token):

    patients_url = BASE_URL + ENDPOINT_PATIENTS_SUMMARY
    patients = self.get_paged_data(token, patients_url)

    return patients


  def get_paged_data(self, token, data_url):

    data = []
    headers = self.get_auth_headers(token)

    while data_url:
      response = requests.get(data_url, headers=headers)
      response.raise_for_status()
      json = response.json()
      data.extend(json['results'])

      data_url = json['next'] # A JSON null on the last page

    return data


  # headers - Authorization
  def get_auth_headers(self, token):
    access_token = token['access_token']
    header_authorization = 'Bearer %s' % access_token

    return {
      'Authorization': header_authorization,
    }



