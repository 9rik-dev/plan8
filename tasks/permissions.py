#!/usr/bin/env python3

from rest_framework.permissions import BasePermission


class AccessPermission(BasePermission):

    message = ""

    def has_permission(self, request, view) -> bool:
        # Allow reads for Managers and Developers
        if request.method in SAFE_METHODS:
            return True
        # Only Mangers can POST or PUT
        return request.is_manager


    def has_object_permission(self, request, view, obj) -> bool:
        return True
        if request.user.role == 1:
            pass

class DeveloperAccessPermission(BasePermission):
    
    def has_permission(self, request, view) -> bool:
        print("has_permission() from DeveloperAccessPermission called")
        print(type(request.method))
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        print("has_object_permission() from DeveloperAccessPermission called")

        # if request.method in permissions.SAFE:
        #     return True
        # else:
        #     # If current logged in User is assigned Developer 
        #     if obj.executor == request.user:
        #         pass
        return True

class ManagerAccessPermission(BasePermission):
    print("has_permission() from ManagerAccessPermission called")

    def has_permission(self, request, view) -> bool:
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        print("has_object_permission() from ManagerAccessPermission called")

        # if request.method in permissions.SAFE:
        #     return True
        # else:
        #     # If current logged in User is assigned Developer 
        #     if obj.executor == request.user:
        #         pass
        return True

