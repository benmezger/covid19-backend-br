from django.urls import include, path

from .api import urls

app_name = "authentication"
urlpatterns = [path("api/", include(urls))]
