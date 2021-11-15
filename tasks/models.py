from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
    )


class Task(models.Model):

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
    manager = models.ManyToManyField(
        "Account", related_name="creator")
    developers = models.ManyToManyField(
        "Account", related_name="developers", blank=True)  # null=True has no effect

    class Meta:
        ordering = ["creation_date"]
        unique_together = (
            # Can't create same tasks, manager can't create task with existing title
            ("title", "description"))

    def __str__(self):
        return f"{self.id}: {self.title}"


class AccountManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **fields):
        if not email:
            raise ValueError("Email is mandatory")
        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_manager', True)
        return self.create_user(email, password, **fields)

# already inherit PermissionsMixin
class Account(AbstractUser):

    """Uses email for authentication
    Default user Role -> developer (is_manager=False)
    """

    username        = None
    email           = models.EmailField("email", unique=True)
    is_manager      = models.BooleanField("manager", default=False)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # login field, logic
    REQUIRED_FIELDS = ["first_name", "last_name"]  # email already required

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    class Roles:
        developer = {"status",}
        manager = {"description", "status",
            "priority", "developers"}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_manager:
            self.writable_fields = self.Roles.manager
        else:
            self.writable_fields = self.Roles.developer

    def __str__(self):
        return f"{self.id}, {self.email}\n{self.is_manager = :}\n{self.writable_fields}\n"

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


all_models = [Task]

