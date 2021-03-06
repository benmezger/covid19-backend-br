from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Covid19 backend API",
        default_version="v1",
        description="Documentation for Covid19-backend endpoints.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")),
    path("", include("notification.urls")),
    path("", include("rules.urls")),
    path("", include("tracking.urls")),
    path("", include("subscribe.urls")),
    # Enables the DRF browsable API page
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
