from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("person", views.PersonViewSet, basename="person")

urlpatterns = [] + router.urls
