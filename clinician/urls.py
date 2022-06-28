from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clinician import views

router = DefaultRouter()

clinician_viewset = views.ClinicianViewset.as_view({'get': 'list', 'post': 'create'})

available_slots_list = views.ClinicianAvailabilityViewset.as_view({'get': 'list', 'post': 'create'})
available_slot_details = views.ClinicianAvailabilityViewset.as_view({'get': 'retrieve'})

book_clinician_availability = views.BookClinicianAvailabilityViewset.as_view({'post': 'create', 'get': 'list'})


urlpatterns = [
    path("", include(router.urls)),
    path(r"clinicians/", clinician_viewset),
    path(r"clinicians/<str:clinician_id>/available-slots/", available_slots_list, name="available_slots_list"),
    path(r"clinicians/<str:clinician_id>/available-slots/<str:availability_id>/", available_slot_details, name="available_slot_details"),
    path(r"clinicians/<str:clinician_id>/bookings/", book_clinician_availability, name="book_clinician_availability"),
]