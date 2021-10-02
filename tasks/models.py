from django.db import models


class Task(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateField(
        auto_now_add=True, db_index=True)
    status = models.SmallIntegerField(default=0)
    prior = models.SmallIntegerField(default=0)
    creator = models.ForeignKey(
        "Manager", on_delete=models.CASCADE)
    executor = models.ForeignKey(
        "Developer", on_delete=models.CASCADE)


    class Meta:
        ordering = ["creation_date"]
        unique_together = (
            ("title", "description"))

    def __str__(self):
        return f"{self.id}: {self.title}"


class User(models.Model):

    """Abstact class, does not have a manager,
    can't be instantiated"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        unique_together = (("name", "id"))
        abstract = True


class Developer(User):
    pass

class Manager(User):
    pass

all_models = [Task, Developer, Manager]
