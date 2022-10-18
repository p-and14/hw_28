from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from ads.models import Selection
from users.models import User


class SelectionPermissions(permissions.BasePermission):
    message = "You can only edit your selections"

    def has_permission(self, request, view):
        selection = get_object_or_404(Selection.objects.all(), id=view.kwargs["pk"])
        if request.user.id != selection.owner.id:
            return False
        return True


class AdPermissions(permissions.BasePermission):
    message = "You can only edit your selections or you don't have access rights"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        if request.user.role in [User.ADMIN, User.MODERATOR]:
            return True
        return False
