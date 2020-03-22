from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("person", views.PersonViewSet, basename="person")
router.register("risk-factor", views.RiskFactor, basename="risk-factor")

urlpatterns = [] + router.urls
