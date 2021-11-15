from django.db import models
from django.contrib.auth.models import User


CREATOR_ALLOWED_FIELDS = {"description", "status",
    "priority", "developers"}

DEVELOPER_ALLOWE_FIELDS = {"status"}

MANAGER = 0
DEVELOPER = 1

class Task(models.Model):

    """
    Custom model manager
    class ManagerTasks(models.Manager):
        def get_queryset(self, id):
            return super().get_queryset().filter(creator=id)
    objects = model.Manager()  # default one
    asigned = ManagerTasks()  # custom manger
    """
    status_options = (
        ("open", "Open"), ("developing", "Developing"),
        ("review", "Review"), ("closed", "Closed"))
    priority_options = (
        ("low", "Low"), ("medium", "Medium"),
        ("high", "High"), ("critical", "Critical"))

    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateField(
        auto_now_add=True, db_index=True)
    status = models.CharField(max_length=10,
        choices=status_options, default="open")
    priority = models.CharField(max_length=10,
        choices=priority_options)
    rejected = models.BooleanField(default=False)

    manager = models.ForeignKey("Manager",
        on_delete=models.SET_NULL, null=True, blank=True)

    # creator = models.ManyToManyField(
    #     User, related_name="creator")
    # developers = models.ManyToManyField(
    #     User, related_name="developers", blank=True)


    class Meta:
        ordering = ["creation_date"]
        unique_together = (
            # Can't create same tasks, manager can't create task with existing title
            ("title", "description"))#, ("creator", "title"))

    def __str__(self):
        return f"{self.id}: {self.title}"


class Manager(models.Model):
    writable_fields = {"description", "status",
    "priority", "developers"}
    role = MANAGER
    # account = models.OneToOneField()

class Developer(models.Model):
    role = DEVELOPER
    writable_fields = {"status"}
    task = models.ForeignKey(Task, on_delete=models.SET_NULL,
        null=True, blank=True)
    # account = models.OneToOneField()


all_models = [Task]
