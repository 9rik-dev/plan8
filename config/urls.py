#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    # maybe separate versions by another urlpatterns
    path("api/v1/", include("tasks.urls", namespace="tasks")),

    # Built-in DRF auth page, using for permission testing
    path("auth/", include("rest_framework.urls")),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
