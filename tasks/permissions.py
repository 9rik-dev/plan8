#!/usr/bin/env python3

from rest_framework.permissions import BasePermission


class IsDeveloper(BasePermission):
    
    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE:
            return True
        else:
            # If current logged in User is assigned Developer 
            if obj.executor == request.user:
                pass
        pass

