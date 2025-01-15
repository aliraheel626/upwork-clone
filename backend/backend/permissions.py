from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the logged-in user is the owner of the proposal
        return obj.user == request.user
