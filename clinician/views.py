from clinician.models import Clinician
from clinician.serializers import ClinicianSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response


class ClinicianViewset(viewsets.ModelViewSet):
    """
    Viewset to add, view list and view details of clinicians.
    """
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer

    def __get_default_bad_func_message(self, func):
        return {'message': f'{func} function is not offered in this path.'}

    def update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PUT")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("PATCH")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        default_message = self.__get_default_bad_func_message("DELETE")
        return Response(default_message, status=status.HTTP_404_NOT_FOUND)
