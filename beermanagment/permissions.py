from rest_framework import permissions
from django.contrib.auth.models import Group


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() or request.method in permissions.SAFE_METHODS
    
    def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() or request.method in permissions.SAFE_METHODS


class IsStaffAndReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() and request.method in permissions.SAFE_METHODS
    
    def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') in request.user.groups.all() and request.method in permissions.SAFE_METHODS


class IsNotStaffReadAndWrite(permissions.BasePermission):

     def has_permission(self, request, view):
        return Group.objects.get(name='Staff Users') not in request.user.groups.all() and (request.method in "POST" or request.method in permissions.SAFE_METHODS)


