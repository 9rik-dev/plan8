#!/usr/bin/env python3

from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
    )
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK
    )

SORTS = {
    "date": "creation_date",
    "priority": "prior",
    "status": "status",
    "id": "id"
    }

class APITasks(APIView):

    # permission_classes = [IsAuthenticated]

    # check permissions
    # permission_classes = (IsAuthenticated,)

    # def check_permissions(self, request):
    #     for p in self.get_permissions():
    #         print(p)


    def get(self, request, pk=None, sort_by=None):
        print("--GET--".center(60, "#"))
        # for d in dir(self.request):
        #     try:
        #         print(f"{d} == {getattr(self.request, d)}")
        #     except NotImplementedError:
        #         pass
        # print(f"{request.auth = :}")
        # print(f"{request.user = :}")
        if request.method == "GET":
            print("KEK")
        print(request.META.get("HTTP_AUTHORIZATION", ""))
        print(request.method)
        print(request.user)
        print(f"{request.user.get_all_permissions() = :}")
        print(f"{request.user.get_group_permissions() = :}")
        print(f"{request.user.get_username() = :}")
        # print(f"{request.user.user_permissions() = :}")


        try:
            if pk:
                task = Task.objects.get(pk=pk)
                return Response(TaskSerializer(task).data)

            elif sort_by:  # by default sorted in Model by date
                param = "-" + SORTS[sort_by]
                stasks = Task.objects.order_by(param)
                return Response(TaskSerializer(stasks, many=True).data,
                    status=HTTP_200_OK)

            else:
                tasks = Task.objects.all()
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

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            saved = serializer.save()
            return Response(
                {"success": f"created task with id {saved.id}"},
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


    def delete(self, request, pk=None):
        print("--DELETE--".center(60, "#"))

        return Response(status=HTTP_404_NOT_FOUND)
