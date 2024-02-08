"""vinywaji URL Configuration"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/openid/", include("simple_openid_connect.integrations.django.urls")),
    path("api/", include("vinywaji.api.urls")),
    path("metrics/", include("vinywaji.metrics.urls")),
    path("", include("vinywaji.gui.urls")),
]
