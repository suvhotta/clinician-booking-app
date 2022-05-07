from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clinician import views

router = DefaultRouter()

router.register(r'clinicians', views.ClinicianViewset)

available_slots_list = views.ClinicianAvailabilityViewset.as_view({'get': 'list', 'post': 'create'})
available_slot_details = views.ClinicianAvailabilityViewset.as_view({'get': 'retrieve'})

urlpatterns = [
    path("", include(router.urls)),
    path(r"clinicians/<str:clinician_id>/available-slots/", available_slots_list),
    path(r"clinicians/<str:clinician_id>/available-slots/<str:availability_id>/", available_slot_details),
]