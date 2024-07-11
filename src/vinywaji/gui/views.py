import json
import math

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request: HttpRequest):
        context = {
            "openid_provider_name": settings.OPENID_PROVIDER_NAME,
            "mafiasi_colors": settings.MAFIASI_COLORS,
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
            "mafiasi_colors": settings.MAFIASI_COLORS,
            "title": settings.ORG_NAME,
        }
        if not request.user.is_anonymous:
            context.update({})

        return render(request, "views/profile.html", context)


class WebhookTriggerView(View):
    def get(self, request: HttpRequest, trigger: str):
        return HttpResponse("OK")


def manifest(request):
    if settings.MAFIASI_COLORS:
        theme_color = "#02837c"
    else:
        theme_color = "#ff8f00"

    content = {
        "name": settings.ORG_NAME,
        "short_name": settings.ORG_NAME,
        "theme_color": theme_color,
        "background_color": "#ffffff",
        "display": "standalone",
        "orientation": "portrait",
        "scope": "/",
        "start_url": "/",
    }

    return HttpResponse(json.dumps(content), content_type="application/json")
