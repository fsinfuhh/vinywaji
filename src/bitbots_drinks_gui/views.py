from django.http import HttpRequest
from django.views import View
from django.shortcuts import render


class DashboardView(View):
    def get(self, request: HttpRequest):
        return render(request, "views/dashboard.html")
