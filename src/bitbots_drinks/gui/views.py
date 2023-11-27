import math

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request: HttpRequest):
        context = {
            "mafiasi_colors": settings.MAFIASI_COLORS,
        }
        if not request.user.is_anonymous:
            context.update({
                "pay_up_amount": 0
                if request.user.current_balance >= 0
                else request.user.current_balance / -100,
                "current_balance": request.user.current_balance / 100,
                "transactions": request.user.transactions.order_by("-time")[:50],
                "default_amount": settings.DEFAULT_AMOUNT,
            })

        return render(request, "views/dashboard.html", context)
