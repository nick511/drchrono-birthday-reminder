
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .scripts.drchrono import DrChronoClient
from .models import Patient
from .serializers import PatientSerializer


def index(request):

  client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)


  if request.session.has_key('token'):
    patients = client.get_patients(request.session.get('token'))

    for patient in patients:
      PatientSerializer.update_from_data(patient)

  else:
    code = request.GET.get('code')
    if code:
      request.session['token'] = client.get_token(code)


  vm = {
    'redirect_url': client.get_authorize_url()
  }

  return render(request, 'birthdayReminder/index.html', vm)




