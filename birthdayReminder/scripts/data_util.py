
import datetime

from django.conf import settings

from ..models import User
from ..serializers import PatientSerializer
from .drchrono import DrChronoClient

def update_all_patients():

  users = User.objects.all() # .distinct('doctor')

  for user in users:
    update_patients(user, refresh_token=user.refresh_token)


def update_patients(user, **kwargs):

  client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)

  # refresh_token
  if kwargs and kwargs['refresh_token']:
    token = client.refresh_token(kwargs['refresh_token'])
    user.access_token = token['access_token']
    user.refresh_token = token['refresh_token']

  # update patients data
  patients_update_time = datetime.datetime.now()
  patients_json = client.get_patients(user.access_token, {'since': user.patients_update_time})
  patients = []
  for patient in patients_json:
    patients.append(PatientSerializer.update_from_data(patient))

  # update patients_update_time
  user.patients_update_time = patients_update_time
  user.save()

  return patients


