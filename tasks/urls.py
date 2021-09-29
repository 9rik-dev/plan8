#!/usr/bin/env python3

from django.urls import path
from .views import APITasks

urlpatterns = [
    path("", APITasks.as_view()),
    path("<int:pk>", APITasks.as_view()),
    # TODO: change this, DRF can handle sorts
    path("<str:sort_by>", APITasks.as_view()),
]
