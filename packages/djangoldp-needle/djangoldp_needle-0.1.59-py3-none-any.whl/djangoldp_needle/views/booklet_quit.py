import json

from djangoldp.views import LDPViewSet
from django.conf import settings
from djangoldp_account.models import LDPUser

from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from ..models import Booklet


class BookletQuitViewset(LDPViewSet):
    def create(self, request, *args, **kwargs):
        booklet = Booklet.objects.get(pk=kwargs['pk'])
        if request.user not in booklet.contributors.all():
            raise NotFound()

        booklet.contributors.remove(request.user)

        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(booklet)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)

