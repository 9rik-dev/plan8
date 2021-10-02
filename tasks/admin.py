from django.contrib import admin
from .models import all_models


for m in all_models:
    admin.site.register(m)
