#!/usr/bin/env python3

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
    )
from .models import Developer, Manager, Task


class DeveloperSerializer(ModelSerializer):
    class Meta:
        model = Developer
        fields = ("id", "name")


class ManagerSerializer(ModelSerializer):
    class Meta:
        model = Manager
        fields = ("id", "name")


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "creation_date",
            "status",
            "prior",
            # "creator",
            # "executor",
            )
        # Supplied without 'fields' variable
        # exclude = ["fieldnames"]


        # This causes not null constraint error
        # depth = 2


    def validate(self, data):
        """Called from POST and PUT methods

        data -> contains any valid fields or nothing for
            empty request or invalid fields request

        """
        print("validate() called")
        # print(data)
        # if len(data) == 0:
        #     raise ValidationError("No valid fields supplied.")
        return data
