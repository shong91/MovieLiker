from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("?", obj.author.__class__)
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS 는 db 를 수정하지 않는 GET, HEAD, OPTIONS 등.
            return True
        elif request.user.is_authenticated:
            # isAuthenticated -? able to CRUD
            if request.user.is_staff:
                return True
            elif obj.__class__ == get_user_model():
                print("obj: ", obj)
                print("user: ", request.user)
                return obj.id == request.user.id
            return False
        else:
            return False


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS 는 db 를 수정하지 않는 GET, HEAD, OPTIONS 등.
            return True
        elif request.user.is_authenticated:
            # isAuthenticated -? able to CRUD
            if request.user.is_staff:
                return True
            elif obj.author.__class__ == get_user_model():
                return obj.id == request.user.id
            return False
        else:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:  # SAFE_METHODS 는 db 를 수정하지 않는 GET, HEAD, OPTIONS 등.
                return True
            elif request.user.is_staff:
                return True
            else:
                return False
        else:
            return False
