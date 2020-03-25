from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("person", views.PersonViewSet, basename="person")
router.register("risk-factor", views.RiskFactorViewSet, basename="risk-factor")
router.register("symptom", views.SymptomViewSet, basename="symptom")
router.register("encounter", views.EncounterViewSet, basename="encounter")

urlpatterns = [
    path(route="infected-persons", view=views.infected_persons, name="infected-persons")
] + router.urls
