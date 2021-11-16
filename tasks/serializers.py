#!/usr/bin/env python3

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CurrentUserDefault,
    PrimaryKeyRelatedField,
    HiddenField,
    SerializerMethodField,
    )
from .models import Task



# class SongSerializer(serializers.ModelSerializer):
#     singer = SingerSerializer(read_only=True)
#     singer_id = SlugRelatedField(queryset=Singer.objects.all(), slug_field='singer', write_only=True)

#     class Meta:
#         model = Singer
#         fields = ['singer', 'signer_id']


class TaskSerializer(ModelSerializer):
    # creator = SerializerMethodField()
    # manager = 
    # developers = 
    class Meta:
        model = Task
        # add readonly for id, date
        # fill in creator automatically from request.user

        fields = (#"__all__"
            "id",
            "title",
            "description",
            "creation_date",
            "status",
            # "rejected",
            "priority",
            "manager",
            "developers",
            )
        read_only_fields = ("creation_date", "id")
        extra_kwargs = {
        "developers": {"required": False}
        }
        # Supplied without 'fields' variable
        # exclude = ["rejected"]

    # def create(self, validated_data):
    #     print("create() called")
    #     print(type(validated_data))
    #     return super().create(validated_data)

        # This causes not null constraint error
        # depth = 2


    def validate(self, data):
        """Called from POST and PUT methods

        data -> contains any valid fields or nothing for
            empty request or invalid fields request

        """
        print(self.context)
        print(self.context["request"].method)
        print(type(self.context["request"].method))
        print("validate() called")
        print(data)
        print(dir(self.Meta))
        # print(data)
        # if len(data) == 0:
        #     raise ValidationError("No valid fields supplied.")
        return data

    # def get_creator(self, obj):
    #     # obj -> Tasks model instance, obj.creator -> ManyToMany Manager
    #     # print(obj.creator, "Serializer")
    #     print(obj.creator.first(), "Serializer")
    #     return obj.creator.first().username
