#!/usr/bin/env python3

from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,)
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,)
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import serializers

from .permissions import (
    ManagerAccessPermission,
    DeveloperAccessPermission,
    )


# SORTS = {
#     "date": "creation_date",
#     "priority": "prior",
#     "status": "status",
#     "id": "id"
#     }


def print_attrs(obj):
    for attr in dir(obj):
        if attr.startswith("__"):
            continue
        try:
            smth = getattr(obj, attr)
        except NotImplementedError:
            continue
        print(f"{attr} = {smth}")


class APITasks(APIView):

    ordering_fields = {"creation_date", "priority", "status", "id"}

    # def check_permissions(self, request):
    #     """Called before request handler is called,
    #     calls Permission.has_permission() for each
    #     permission
    #     """

    #     pass

    # def check_object_permissions(self, request, obj):
    #     """Must be called explicitly,
    #     calls Permission.has_object_permission
    #     for each permission"""
    #     pass


    def assign_developers(*devs):
        # 
        q = Developers.objects.in_bulk(devs)
        task.developers
        pass

    def has_access_to_fields(request) -> bool:

        pass


    def get_ordered_by(self, params):
        # if len(params) > 1:
        #     raise Exception("Multiple sorts not Allowed")  # multiple orders not allowed 
        order = params.get("ordering", "id")
        print(f"{order = :}")
        if order.strip("-") not in self.ordering_fields:
            raise Exception("Unsupported fields")  # unsupported fields
        q = Task.objects.order_by(order)
        print(f"{order = :}")
        print(q)
        return q


    permission_classes = (IsAuthenticated,
        ManagerAccessPermission,
        DeveloperAccessPermission,)

    # check permissions
    # permission_classes = (IsAuthenticated,)

    # def check_permissions(self, request):
    #     for p in self.get_permissions():
    #         print(p)

    # def perform_create(self, serializer):
    #     serializer.validated_data["creator"] = self.request.user.id
    #     return super().perform_create(serializer)


    def get(self, request, pk=None, sort_by=None):
        print("--GET--".center(60, "#"))
        print(request.query_params)
        # print(request.query_params.get("ordering", "id"))
        # print_attrs(request)

        # print(dir(request.user))

        # breakpoint()
        # for d in dir(self.request):
        #     try:
        #         print(f"{d} == {getattr(self.request, d)}")
        #     except NotImplementedError:
        #         pass
        # print(f"{request.auth = :}")
        # print(f"{request.user = :}")
        # if request.method == "GET":
        #     print("KEK")
        # print(request.META.get("HTTP_AUTHORIZATION", ""))
        # print(request.method)
        # print(request.user)
        # print(request.user.id)
        # print(f"{request.user.get_all_permissions() = :}")
        # print(f"{request.user.get_group_permissions() = :}")
        # print(f"{request.user.get_username() = :}")
        # print(f"{request.user.user_permissions() = :}")


        try:
            if pk:
                task = Task.objects.get(pk=pk)
                return Response(TaskSerializer(task).data)

            # elif sort_by:  # by default sorted in Model by date
            #     param = "-" + SORTS[sort_by]
            #     tasks = Task.objects.order_by(param)
            #     return Response(TaskSerializer(tasks).data,
            #         status=HTTP_200_OK)

            else:
                # tasks = Task.objects.all()
                tasks = self.get_ordered_by(request.query_params)
                return Response(TaskSerializer(tasks, many=True).data,
                    status=HTTP_200_OK)


        except Task.DoesNotExist:  # invalid pk
            err = {"entry_errors": [f"entry with id <{pk}> does not exist",]}
        except KeyError:  # invalid sort
            err = {"sort_errors": [f"sort by <{sort_by}> not allowed",]}
        return Response(err, status=HTTP_404_NOT_FOUND)


    # TODO: prettify rest_framework.exceptions.ValidationError
    def post(self, request):

        print("--POST--".center(60, "#"))
        # print(request.META.get("HTTP_AUTHORIZATION", ""))
        # print(request.method)
        # print(request.user)
        # print(request.user.id)
        # print(f"{request.user.get_all_permissions() = :}")
        # print(f"{request.user.get_group_permissions() = :}")
        # print(f"{request.user.get_username() = :}")
        print(request.user)
        print(type(request.user))
        request.data["manager"] = request.user.id
        print(request.data)
        serializer = TaskSerializer(data=request.data,
            context={"request": request})
        if serializer.is_valid():
            # create() in validator is called only if save() called
            saved = serializer.save()
            # saved = 3
            return Response(
                {"success": f"created task with id {saved.id}"},
                # {"success": f"created task with id {saved}"},
                status=HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=HTTP_400_BAD_REQUEST)


    # Veird behaviour with read_only and auto_add fields
    # it accepts them but doesn't do anything
    def put(self, request, pk, format=None):
        print("--PUT--".center(60, "#"))

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExits:
            err = {"error": f"entry with id <{pk}> does not exist"}
            return Response(err)
        # Source suggests that on update you can ommit instance
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            print(f"{serializer.initial_data = :}")
            print(f"{serializer.validated_data = :}")
            print(f"{serializer.errors = :}")
            # print(f"{serializer.data = :}")
            serializer.save()
            return Response(serializer.data,
                status=HTTP_200_OK)
        return Response(serializer.errors,
            status=HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        print("--DELETE--".center(60, "#"))
        task = get_object_or_404(Task.objects, pk=pk)
        task.delete()
        return Response(status=HTTP_204_NO_CONTENT)
