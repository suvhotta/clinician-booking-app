from django.urls import path, include
from rest_framework.routers import DefaultRouter

from patient import views


router = DefaultRouter()

router.register(r'patients', views.PatientViewset)

urlpatterns = [
    path("", include(router.urls))
]
