import math

from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request: HttpRequest):
        if request.user.is_anonymous:
            context = {}
        else:
            context = {
                "pay_up_amount": 0
                if request.user.current_balance >= 0
                else math.ceil(request.user.current_balance / -100),
                "current_balance": request.user.current_balance / 100,
                "transactions": request.user.transactions.order_by("-time")[:50],
            }

        return render(request, "views/dashboard.html", context)
