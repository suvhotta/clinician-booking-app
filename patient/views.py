from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from patient.models import Patient
from patient.serializers import PatientSerializer


class PatientViewset(viewsets.ModelViewSet):
    """
    Viewset to add, view list and view details of patients.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def __get_default_bad_func_message(self, func):
        return {'message': f'{func} function is not offered in this path.'}

    def update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PUT")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PATCH")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        patient = get_object_or_404(Patient, pk=pk)
        patient.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)