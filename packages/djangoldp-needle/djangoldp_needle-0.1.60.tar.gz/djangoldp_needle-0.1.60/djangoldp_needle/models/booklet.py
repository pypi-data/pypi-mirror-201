from django.conf import settings
from django.db import models
from djangoldp.models import Model
from . import Annotation, Tag
from ..permissions import BookletPermissions


class Booklet(Model):
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="boolket_owner")
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="boolket_contributor")
    annotations = models.ManyToManyField(Annotation, related_name="booklets")
    title = models.CharField(max_length=160)
    abstract = models.CharField(max_length=4096, null=True)
    accessibility_public = models.BooleanField()
    collaboration_allowed = models.BooleanField()
    tags = models.ManyToManyField(Tag)
    cover = models.IntegerField()

    class Meta(Model.Meta):
        rdf_type = 'hd:annotation'
        #rdf_context = 'https://www.w3.org/ns/anno.jsonld'
        owner_field = "owners"
        owner_perms = []
        authenticated_perms = []
        anonymous_perms = []
        permission_classes = [BookletPermissions]