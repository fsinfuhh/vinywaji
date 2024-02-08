import logging
from http import HTTPStatus
from ipaddress import ip_address

import prometheus_client.exposition
from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from prometheus_client.registry import REGISTRY

logger = logging.getLogger(__name__)


class PrometheusMetricsView(View):
    def is_allowed(self, request: HttpRequest) -> bool:
        """Whether the requestor is allowed to access this view"""
        if settings.TRUST_REVERSE_PROXY and "HTTP_X_FORWARDED_FOR" in request.META.keys():
            x_forwarded_for = request.META["HTTP_X_FORWARDED_FOR"]
            remote_ip = ip_address(x_forwarded_for.split(",")[0])
        else:
            remote_ip = ip_address(request.META["REMOTE_ADDR"])

        return any(remote_ip in net for net in settings.ALLOWED_METRICS_NETS)

    def get(self, request: HttpRequest) -> HttpResponse:
        if not self.is_allowed(request):
            return HttpResponse(status=HTTPStatus.FORBIDDEN)

        encode, content_type = prometheus_client.exposition.choose_encoder(request.META["HTTP_ACCEPT"])
        content = encode(REGISTRY)
        return HttpResponse(status=HTTPStatus.OK, content=content, content_type=content_type)
