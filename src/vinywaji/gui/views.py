import json
import math

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from vinywaji.core.models import WebhookConfig


class DashboardView(View):
    def get(self, request: HttpRequest):
        context = {
            "openid_provider_name": settings.OPENID_PROVIDER_NAME,
            "title": settings.ORG_NAME,
        }
        if not request.user.is_anonymous:
            context.update(
                {
                    "pay_up_amount": 0
                    if request.user.current_balance >= 0
                    else request.user.current_balance / -100,
                    "current_balance": request.user.current_balance / 100,
                    "transactions": request.user.transactions.order_by("-time")[:50],
                    "default_amount": settings.DEFAULT_AMOUNT,
                }
            )

        return render(request, "views/dashboard.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        context = {
            "openid_provider_name": settings.OPENID_PROVIDER_NAME,
            "title": settings.ORG_NAME,
        }
        if not request.user.is_anonymous:
            context.update(
                {
                    "webhooks": request.user.webhooks.all(),
                }
            )

        return render(request, "views/profile.html", context)


class WebhookTriggerView(View):
    def get(self, request: HttpRequest, trigger: str):
        webhook = WebhookConfig.objects.filter(trigger_key=trigger)
        if len(webhook) == 1:
            webhook[0].trigger()
            return HttpResponse("OK", status_code=200)
        else:
            return HttpResponse("Failed", status_code=404)


def manifest(request):
    content = {
        "name": settings.ORG_NAME,
        "short_name": settings.ORG_NAME,
        "background_color": "#ffffff",
        "display": "standalone",
        "orientation": "portrait",
        "scope": "/",
        "start_url": "/",
    }

    return HttpResponse(json.dumps(content), content_type="application/json")
