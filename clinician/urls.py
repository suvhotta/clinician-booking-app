from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clinician import views

router = DefaultRouter()

router.register(r'clinicians', views.ClinicianViewset)

available_slots_list = views.ClinicianAvailabilityViewset.as_view({'get': 'list', 'post': 'create'})
available_slot_details = views.ClinicianAvailabilityViewset.as_view({'get': 'retrieve'})

book_clinician_availability_create = views.BookClinicianAvailabilityViewset.as_view({'post': 'create'})
book_clinician_availability_list = views.BookClinicianAvailabilityViewset.as_view({'get': 'list'})


urlpatterns = [
    path("", include(router.urls)),
    path(r"clinicians/<str:clinician_id>/available-slots/", available_slots_list),
    path(r"clinicians/<str:clinician_id>/available-slots/<str:availability_id>/", available_slot_details),
    path(r"clinicians/<str:clinician_id>/available-slots/<str:availability_id>/bookings/", book_clinician_availability_create),
    path(r"clinicians/<str:clinician_id>/bookings/", book_clinician_availability_list),
]