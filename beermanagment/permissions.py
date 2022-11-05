from django.contrib.auth.models import Group
from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() or request.method in permissions.SAFE_METHODS


class IsStaffAndReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() and request.method in permissions.SAFE_METHODS


class IsNotStaffWriteOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') not in request.user.groups.all() and (request.method in permissions.SAFE_METHODS or request.method == "POST")
