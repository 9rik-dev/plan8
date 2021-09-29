#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # maybe separate versions by another urlpatterns
    path("api/v1/", include("tasks.urls"))
]
