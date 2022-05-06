from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clinician import views

router = DefaultRouter()

router.register(r'clinicians', views.ClinicianViewset)

urlpatterns = [
    path("", include(router.urls))
]