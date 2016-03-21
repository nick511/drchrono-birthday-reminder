
import kronos, datetime

from django.core.mail import send_mass_mail

from .models import Patient
from .scripts.data_util import update_all_patients

# Run tasks manually: $ python manage.py birthdayReminder
@kronos.register('0 8 * * *')
def birthdayReminder():

  update_all_patients()

  # get today's star
  today = datetime.date.today()
  patients = Patient.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)

  # send message
  messages = ()
  for patient in patients:
    if patient.email:
      msg = ('Happy Birthday', 'Happy Birthday, %s' % patient.first_name, 'happybirthday@drchrono.com', [patient.email])
      messages += (msg,)

  send_mass_mail(messages, fail_silently=False)




