#!/usr/bin/env python3

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
    )
from .models import Task



class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        # add readonly for id, date
        # fill in creator automatically from request.user
        fields = (
            "id",
            "title",
            "description",
            "creation_date",
            "status",
            "priority",
            # "creator",
            "developers",
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
