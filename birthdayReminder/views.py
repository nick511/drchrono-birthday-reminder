
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .scripts.drchrono import DrChronoClient



def index(request):

  client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)

  code = request.GET.get('code')
  if code:
    request.session['token'] = client.get_token(code)

  if request.session.has_key('token'):
    client.get_patients_summary(request.session.get('token'))


  vm = {
    'redirect_url': client.get_authorize_url()
  }

  return render(request, 'birthdayReminder/index.html', vm)




