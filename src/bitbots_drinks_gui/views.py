import math

from django.http import HttpRequest
from django.views import View
from django.shortcuts import render


class DashboardView(View):
    def get(self, request: HttpRequest):
        return render(
            request,
            "views/dashboard.html",
            {
                "pay_up_amount": 0
                if request.user.current_balance >= 0
                else math.ceil(request.user.current_balance / -100),
                "current_balance": request.user.current_balance / 100,
            },
        )
