from django.urls import path, include

from .v1 import urls


urlpatterns = [path("v1/", include(urls))]
