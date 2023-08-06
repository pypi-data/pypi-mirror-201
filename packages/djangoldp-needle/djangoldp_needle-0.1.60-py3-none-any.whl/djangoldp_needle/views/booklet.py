from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet

from django.db.models import Q
from rest_framework.generics import get_object_or_404

from ..models import Booklet


class BookletSerializer(LDPSerializer):
    @property
    def with_cache(self):
        return False

class BookletViewset(LDPViewSet):
    serializer_class = BookletSerializer
    fields = [
        '@id',
        'owners',
        'contributors',
        'annotations',
        'title',
        'abstract',
        'accessibility_public',
        'collaboration_allowed',
        'tags',
        'cover'
    ]
    def perform_create(self, serializer, **kwargs):
        booklet = super().perform_create(serializer, **kwargs)
        booklet.owners.add(self.request.user)

        return booklet

    def get_queryset(self, *args, **kwargs):
        user = self.request.user

        if user.is_anonymous:
            return Booklet.objects.filter(accessibility_public=True)

        return Booklet.objects.filter(Q(owners__in=[user])
                                      | Q(contributors__in=[user])
                                      | (Q(collaboration_allowed=True) & Q(annotations__creator=user) )
                                      ).distinct()

    def get_object(self):

        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=self.kwargs['pk'])

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj