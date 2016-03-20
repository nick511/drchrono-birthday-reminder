
from rest_framework import serializers

from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
  class Meta:
      model = Patient
      fields = ('id', 'doctor', 'first_name', 'last_name', 'chart_id', 'date_of_birth', 'gender', 'email')

  @staticmethod
  def update_from_data(data):
      patient, created = Patient.objects.get_or_create(pk=data['id'])
      patient = PatientSerializer(patient, data)
      if patient.is_valid():
        patient.save()

      return patient