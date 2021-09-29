#!/usr/bin/env python3

from rest_framework.serializers import ModelSerializer
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
            "creator",
            "executor"
            )
        depth = 2
