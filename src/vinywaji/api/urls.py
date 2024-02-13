from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerOauthRedirectView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"transactions", views.TransactionViewSet, basename="transaction")


urlpatterns = [
    path("schema", SpectacularAPIView.as_view(), name="openapi_schema"),
    path(
        "schema/swagger",
        SpectacularSwaggerView.as_view(url_name="openapi_schema"),
        name="swagger-ui",
    ),
    path(
        "schema/oauth2-redirect.html",
        SpectacularSwaggerOauthRedirectView.as_view(),
        name="swagger-ui-oauth-callback",
    ),
] + router.urls
