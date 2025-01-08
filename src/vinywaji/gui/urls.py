from django.urls import path

from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("webhook/<str:trigger>", views.WebhookTriggerView.as_view(), name="webhook-trigger"),
    path("manifest.json", views.manifest, name="manifest"),
]
