
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from datetime import datetime

from .scripts.drchrono import DrChronoClient
from .scripts.data_util import update_patients
from .serializers import UserSerializer
from .models import Patient


client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)

def index(request):

  if request.GET.get('code'):
    request.session['token'] = client.get_token(request.GET.get('code'))
    return redirect('update')


  vm = {
    'redirect_url': client.get_authorize_url()
  }

  return render(request, 'birthdayReminder/index.html', vm)

def update(request):

  client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)

  if request.session.has_key('token'):
    token = request.session.get('token')
    access_token = token['access_token']

    # update user data
    user_data = client.get_current_user(access_token)
    user_data['access_token'] = access_token
    user_data['refresh_token'] = token['refresh_token']
    user = UserSerializer.update_from_data(user_data)

    patients = update_patients(user)

    vm = {
      'updated_count': len(patients),
      'scheduled_count': Patient.objects.filter(doctor=user.doctor).count()
    }

    return render(request, 'birthdayReminder/update.html', vm)



