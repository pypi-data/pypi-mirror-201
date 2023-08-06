import json

from djangoldp.views import LDPViewSet
from django.conf import settings
from djangoldp_account.models import LDPUser

from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from ..models import Booklet


class BookletInvitationViewset(LDPViewSet):
    def create(self, request, *args, **kwargs):
        booklet = Booklet.objects.get(pk=kwargs['pk'])
        if request.user not in booklet.owners.all():
            raise NotFound()
        try:
            target = LDPUser.objects.get(email=request.data['email'])
        except LDPUser.DoesNotExist as e:
            raise ValidationError(detail="Invalid email")
        booklet.contributors.add(target)

        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(booklet)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

