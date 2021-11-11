from django.db import models
from django.contrib.auth.models import User


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
    # status = models.SmallIntegerField(default=0)
    status = models.CharField(max_length=10,
        choices=status_options, default="open")
    # prior = models.SmallIntegerField(default=0)
    priority = models.CharField(max_length=10,
        choices=priority_options)
    # creator = models.ForeignKey(
    #     "Manager", on_delete=models.CASCADE)
    developers = models.ForeignKey(
        User, on_delete=models.PROTECT)


    class Meta:
        ordering = ["creation_date"]
        unique_together = (
            ("title", "description"))

    def __str__(self):
        return f"{self.id}: {self.title}"

all_models = [Task]
