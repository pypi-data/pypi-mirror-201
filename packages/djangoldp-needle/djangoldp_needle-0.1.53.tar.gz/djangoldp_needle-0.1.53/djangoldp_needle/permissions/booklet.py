from djangoldp.permissions import LDPPermissions


class BookletPermissions(LDPPermissions):
    def get_container_permissions(self, request, view, obj=None):
        perms = super().get_container_permissions(request, view, obj)
        perms.add('view')
        return perms


    def get_object_permissions(self, request, view, obj):
        if request.user.is_anonymous:
            perms = set()
            if obj.accessibility_public:
                perms.add('view')
            return perms

        perms = super().get_object_permissions(request, view, obj)
        if obj.collaboration_allowed:
            perms.add('view')

        if request.user in obj.owners.all():
            perms.add('change')
            perms.add('view')

        if request.user in obj.contributors.all():
            perms.add('change')
            perms.add('view')
        return perms