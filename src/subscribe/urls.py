from django.urls import include, path

from .api import urls

urlpatterns = [path("api/", include(urls))]
