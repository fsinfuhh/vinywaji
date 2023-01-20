"""bitbots_drinks URL Configuration"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/openid/", include("simple_openid_connect.integrations.django.urls")),
    path("api/", include("bitbots_drinks.api.urls")),
    path("", include("bitbots_drinks.gui.urls")),
]
