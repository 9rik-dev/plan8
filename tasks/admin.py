#!/usr/bin/env python3
from django.contrib.auth.admin import (
    UserAdmin,)
from django.contrib import admin
from .models import Task, Account
from .forms import AccountCreationForm, AccountChangeForm



def perms_factory(on_none=True):
    def wrapped(self_inst, request, obj=None):
        if obj is None:
            return on_none
        return obj.is_manager
    return wrapped


# Throws an exception when changing User Role in admin
class ManagedTasksInline(admin.StackedInline):

    model = Task
    max_num = 2
    verbose_name = "Managed Task"
    verbose_name_plural = "Managed Tasks"
    classes = ("wide", "no-upper")  # Capitalize header

    # Should return False when obj=None
    has_view_permission = perms_factory(False)
    # Rest should return True when obj=None
    has_add_permission = perms_factory()
    has_change_permission = perms_factory()
    has_delete_permission = perms_factory()



class AccountAdmin(UserAdmin):

    # form = AccountChangeForm
    # add_form = AccountCreationForm

    model = Account

    list_display = ("email", "id", "is_manager", "assigned_to", "tasks_display")
    list_filter = ("email", "is_manager")
    list_editable = ("is_manager",)
    # Without explicit ordering, admin will use username,
    # which is not defined in custom User model
    ordering = ("id",)
    inlines = (ManagedTasksInline,)
    fieldsets = (
        # *UserAdmin.fieldsets,
        ("Account", {"fields": ("email",)}),#, "password")}),
        ("Info", {"fields": ("first_name", "last_name")}),
        ("Roles", {"fields": ("is_superuser", "is_manager",
            "is_staff", "is_active")}),
        ("Tasks", {"fields": ("assigned_to",)}),
        # ("Projects", {"fields": ("task", "task_set")})
        )
    add_fieldsets = (
        ("Account", {
            "classes": ("wide",),
            "fields": ("email", "password", "is_active",
                "is_manager", "is_staff", "is_superuser")},
            ),
        )

    def tasks_display(self, obj):
        return [str(t) for t in obj.managed_tasks.all()]
    tasks_display.short_description = "Tasks"


    class Media:  # Got annoyed by CAPS in InlineForm
        css = {"all": ("inline.css",)}


    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     print("#" * 60, "kek")
    #     print("lol", db_field, request, **kwargs)
    #     print("kek")
    #     if db_field.name == "managed_tasks":
    #         kwargs["queryset"] = Account.objects.managed_tasks.all()
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def has_module_permission(self, request):
    #     # return False
    #     print(dir(request))
    #     print(request.user.is_manager)
    #     print("kekekjahdlkjsahdla")
    #     return request.user.is_manager


class TaskAdmin(admin.ModelAdmin):
    model = Task
    date_hierarchy = "creation_date"
    list_display = ("id", "title", "description")#, "mans",  "devs", "creation_date", "status", "priority")
    ordering = ("id",)
    search_fields = ("title",)

    # Restrict Manager dropdown to show only 'managers'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manager":
            kwargs["queryset"] = Account.objects.filter(is_manager=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Set 'manager' field read-only after creation
    def get_readonly_fields(self, request, obj=None):
        return ["manager"] if obj else []

    def developers_display(self, obj):
        return obj.developers.all()
    developers_display.short_description = "Developers"


admin.site.register(Account, AccountAdmin)
admin.site.register(Task, TaskAdmin)


admin.site.site_header = "Plan8's Admin Panel"
admin.site.site_title = "88888888"
admin.site.index_title = "Welcome!"
