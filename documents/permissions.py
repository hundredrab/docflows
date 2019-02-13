from rest_framework.permissions import BasePermission


class IsAllowedToRead(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.viewable_by(request.user.user_prof)


class IsAllowedToWrite(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.shareable_by(request.user.user_prof)
