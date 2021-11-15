from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
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

admin.site.register(Task, TaskAdmin)



admin.site.site_header = "Plan8's Admin Panel"
admin.site.site_title = "88888888"
admin.site.index_title = "Welcome!"
