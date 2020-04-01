from django.urls import include, path

from .v1 import urls

urlpatterns = [path("v1/", include(urls))]
