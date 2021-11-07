from django.urls import path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views


router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"transactions", views.TransactionViewSet, basename="transaction")


urlpatterns = [
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + router.urls
