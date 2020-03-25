from django.urls import path, include

from .api import urls

app_name = "tracking"
urlpatterns = [path("api/", include(urls))]
