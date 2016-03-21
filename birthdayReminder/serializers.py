
from rest_framework import serializers

from .models import Patient, User

class PatientSerializer(serializers.ModelSerializer):
  class Meta:
      model = Patient
      fields = ('id', 'doctor', 'first_name', 'last_name', 'chart_id', 'date_of_birth', 'gender', 'email')

  @staticmethod
  def update_from_data(data):
      model, created = Patient.objects.get_or_create(pk=data['id'])
      serializer = PatientSerializer(model, data)
      if serializer.is_valid():
        serializer.save()
      else:
        print(serializer.errors)

      return model


class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = User
      fields = ('id', 'doctor', 'username', 'patients_update_time', 'access_token', 'refresh_token')

  @staticmethod
  def update_from_data(data):
      model, created = User.objects.get_or_create(doctor=data['doctor'], username=data['username'])
      serializer = UserSerializer(model, data)
      if serializer.is_valid():
        serializer.save()

      return model