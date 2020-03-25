from django.urls import include, path

from .api import urls

app_name = "notification"
urlpatterns = [path("api/", include(urls))]
