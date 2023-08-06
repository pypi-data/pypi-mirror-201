from django.core.exceptions import SuspiciousOperation
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet
from rest_framework import serializers
import base64

from ..models import AnnotationTarget, Annotation

class RequestParserMixin:
    model = Annotation

    def parse_request(self):
        url_encoded = self.kwargs['url'].replace('__', '/')
        url = base64.b64decode(url_encoded).decode('UTF-8')
        return url, self.kwargs['date']

class AnnotationIntersectionsViewset(LDPViewSet, RequestParserMixin):
    def get_queryset(self, *args, **kwargs):
        url_encoded = self.kwargs['url'].replace('__', '/')
        url = base64.b64decode(url_encoded).decode('UTF-8')
        res = Annotation.objects.filter(target__target=url).exclude(creator=self.request.user).order_by(
            "creation_date")

        return res
