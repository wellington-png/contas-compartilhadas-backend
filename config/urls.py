from django.contrib import admin
from django.urls import path, include
from config.router import router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularJSONAPIView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("", include("apps.groups.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
    path(
        "api/schema.json",
        SpectacularJSONAPIView.as_view(),
        name="schema-json",
    ),
]
