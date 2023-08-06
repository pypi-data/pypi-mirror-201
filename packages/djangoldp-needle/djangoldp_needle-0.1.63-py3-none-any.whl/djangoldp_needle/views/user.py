from django.conf import settings
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet, LDPNestedViewSet
from djangoldp_account.models import LDPUser


class UserSerializer(LDPSerializer):
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        if isinstance(obj, LDPUser):
            del rep['email']

        return rep

class UserViewset(LDPViewSet):
    serializer_class = UserSerializer
