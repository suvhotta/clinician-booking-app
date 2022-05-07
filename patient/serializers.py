from rest_framework import serializers
from rest_framework.validators import ValidationError

from app.serializers import UserSerializer
from patient.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        return Patient.objects.create(user=user)

    def validate(self, data):
        super().validate(data)
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise ValidationError(f"Got unexpected fields: {unknown_keys}")
        return data
