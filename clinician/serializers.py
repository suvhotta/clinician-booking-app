from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import ValidationError

from app.serializers import UserSerializer
from clinician.models import (
    ClinicianAvailability,
    Clinician
)


class ClinicianSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Clinician
        fields = ['degree_conferred_date', 'specializations', 'user']

    def validate_degree_conferred_date(self, value):
        if datetime.now().date() <= value:
            raise ValidationError("Please enter a valid degree conferred date")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        clinician = Clinician.objects.create(user=user, **validated_data)
        return clinician

    def __calculate_years_of_exp(self, degree_date):
        return relativedelta(datetime.today(), datetime.strptime(degree_date, "%Y-%m-%d")).years

    def to_representation(self, instance):
        clinician_record = super().to_representation(instance)
        clinician_record['years_of_experience'] = self.__calculate_years_of_exp(clinician_record['degree_conferred_date'])
        clinician_record.update(**clinician_record["user"])
        del clinician_record['degree_conferred_date'], clinician_record["user"]
        return clinician_record


class AvailabilitySerializer(serializers.ModelSerializer):
    clinician = ClinicianSerializer(required=False)
    clinician_id = serializers.UUIDField(format='hex_verbose', write_only=True)

    class Meta:
        model = ClinicianAvailability
        fields = ['clinician', 'is_available', 'start_time', 'end_time', 'clinician_id']
        read_only_fields = ('is_available', 'clinician')

    def create(self, validated_data):
        clinician_id = validated_data.pop('clinician_id')
        clinician = get_object_or_404(Clinician, pk=clinician_id)
        return ClinicianAvailability.objects.create(clinician=clinician, **validated_data)

    def validate(self, data):
        super().validate(data)
        if data['start_time'] >= data['end_time']:
            raise ValidationError("Please enter valid start and end time")
        return data
