from django.urls import path

from . import views

urlpatterns = [
    path("rules/", views.RuleViewSet.as_view(), name="rules-list"),
]
