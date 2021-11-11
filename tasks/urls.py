#!/usr/bin/env python3

from django.urls import path
from .views import APITasks

app_name = "tasks"

urlpatterns = [
    path("", APITasks.as_view(), name="detail_put_delete"),
    path("<int:pk>", APITasks.as_view(), name="list_create"),
    # TODO: change this, DRF can handle sorts
    path("<str:sort_by>", APITasks.as_view()),
]
