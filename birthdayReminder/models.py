
from django.db import models

class Patient(models.Model):
  GENDER = (
        ('', ''),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

  doctor = models.IntegerField(default=0)
  first_name = models.CharField(max_length=100, default='')
  last_name = models.CharField(max_length=100, default='')
  chart_id = models.CharField(max_length=10, default='')
  date_of_birth = models.DateField(blank=True, null=True)
  gender = models.CharField(choices=GENDER, max_length=6)
  email = models.CharField(max_length=200, default='')


  def __str__(self):
    return "%i, %s %s" % (self.id, self.first_name, self.last_name)


class User(models.Model):

  doctor = models.IntegerField(default=0)
  username = models.CharField(max_length=100, default='')
  patients_update_time = models.DateTimeField(default="1970-01-01")
  access_token = models.CharField(max_length=50, default='')
  refresh_token = models.CharField(max_length=50, default='')




