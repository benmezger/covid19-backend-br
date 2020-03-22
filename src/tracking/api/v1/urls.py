from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("person", views.PersonViewSet, basename="person")
router.register("risk-factor", views.RiskFactorViewSet, basename="risk-factor")
router.register("symptom", views.SymptomViewSet, basename="symptom")

urlpatterns = [] + router.urls
