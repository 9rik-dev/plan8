from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Task, Account


class AccountAdmin(UserAdmin):

    # Add two fields 'operate', 'assigned'
    model = Account
    list_display = ("email", "id", "is_manager", "task", "task_set")
    list_filter = ("email", "is_manager")
    list_editable = ("is_manager",)
    # Without explicit ordering, admin will use username,
    # which is not defined in custom User model
    ordering = ("id",)
    fieldsets = (
        # *UserAdmin.fieldsets,
        ("Account", {"fields": ("email",)}),#, "password")}),
        ("Info", {"fields": ("first_name", "last_name")}),
        ("Roles", {"fields": ("is_superuser", "is_manager",
            "is_staff", "is_active")}),
        # ("Tasks", {})
        # ("Projects", {"fields": ("task", "task_set")})
        )
    add_fieldsets = (
        ("Account", {
            "classes": ("wide",),
            "fields": ("email", "password", "is_active",
                "is_manager", "is_staff", "is_superuser")},
            ),
        )

class TaskAdmin(admin.ModelAdmin):
    model = Task
    date_hierarchy = "creation_date"
    list_display = ("id", "title")#, "mans",  "devs", "creation_date", "status", "priority")
    ordering = ("id",)
    search_fields = ("title",)

    # def mans(self, obj):
    #     return None
    #     # m = list(obj.creator.all())
    #     # return m.username if m else "None"

    # def devs(self, obj):
    #     team = list(e.username for e in obj.developers.all())
    #     return team if team else "None"


admin.site.register(Account, AccountAdmin)
admin.site.register(Task, TaskAdmin)



admin.site.site_header = "Plan8's Admin Panel"
admin.site.site_title = "88888888"
admin.site.index_title = "Welcome!"
