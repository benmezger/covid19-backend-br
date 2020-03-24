from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("notification", views.NotificationViewSet, basename="notification")

urlpatterns = [] + router.urls
