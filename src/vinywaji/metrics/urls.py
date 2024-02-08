from django.urls import path

from vinywaji.metrics import views

urlpatterns = [
    path("", views.PrometheusMetricsView.as_view(), name="prometheus_metrics"),
]
