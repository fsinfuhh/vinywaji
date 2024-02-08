import logging
from http import HTTPStatus

import prometheus_client.exposition
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from prometheus_client.registry import REGISTRY

logger = logging.getLogger(__name__)


class PrometheusMetricsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        (encode, content_type) = prometheus_client.exposition.choose_encoder(request.META["HTTP_ACCEPT"])
        content = encode(REGISTRY)
        return HttpResponse(status=HTTPStatus.OK, content=content, content_type=content_type)
