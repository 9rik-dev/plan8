from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
        "date_joined",
        "last_login"
        )
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("date_joined", "last_login")
    
admin.site.register(Account, AccountAdmin)
