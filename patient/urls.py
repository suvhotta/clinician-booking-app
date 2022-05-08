from django.urls import path, include
from rest_framework.routers import DefaultRouter

from patient import views


router = DefaultRouter()

router.register(r'patients', views.PatientViewset)

patient_booking_list = views.PatientBookingViewset.as_view({'get': 'list'})
patient_booking_details = views.PatientBookingViewset.as_view({'get': 'retrieve', 'patch': 'partial_update'})

urlpatterns = [
    path("", include(router.urls)),
    path(r"patients/<str:patient_id>/bookings/", patient_booking_list),
    path(r"patients/<str:patient_id>/bookings/<str:booking_id>/", patient_booking_details),
]
