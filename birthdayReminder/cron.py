
from django.core.mail import send_mass_mail
from django.conf import settings

import kronos, datetime

from .models import User, Patient
from .scripts.drchrono import DrChronoClient

# Run tasks manually: $ python manage.py birthdayReminder
@kronos.register('0 8 * * *')
def birthdayReminder():

  client = DrChronoClient(settings.CLIENT_ID, settings.CLIENT_SECRET, settings.REDIRECT_URI)

  users = User.objects.all() # .distinct('doctor')

  for user in users:
    # refresh_token
    token = client.refresh_token(user.refresh_token)
    user.access_token = token['access_token']
    user.refresh_token = token['refresh_token']

    # update patients data
    patients = client.get_patients(user.access_token, {'since': user.patients_update_time})
    for patient in patients:
      PatientSerializer.update_from_data(patient)

    # update patients_update_time
    user.patients_update_time = datetime.now()
    user.save()


  # get today's star
  today = datetime.date.today()
  patients = Patient.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)

  # send message
  messages = ()
  for patient in patients:
    msg = ('Happy Birthday', 'Happy Birthday, %s' % patient.first_name, 'happybirthday@drchrono.com', [patient.email])
    messages += (msg,)

  send_mass_mail(messages, fail_silently=False)

