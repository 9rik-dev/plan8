from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,)
from django.db.models.signals import post_save


def get_sentinel_manager():
    """Assign first retrieved admin as task manager,
    when manger object is deleted"""
    return get_user_model().objects.filter(is_superuser=True).first()


class A(models.Model):
    opts = (
        (1, "open"), (2, "close"), (3, "maybe"))
    f = models.CharField(max_length=5, choices=opts)

    def __str__(self):
        return self.f

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
    manager = models.ForeignKey("Account",
        related_name="managed_tasks",  # Field name for Account model
        on_delete=models.SET(get_sentinel_manager))
    # developers -> related_name from Account model

    class Meta:
        verbose_name = "task"
        verbose_name_plural = "tasks"
        ordering = ["creation_date"]
        unique_together = (
            # Can't create same tasks,
            # manager can't create task with existing title
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
        fields.setdefault('unassigned', True)
        return self.create_user(email, password, **fields)

# already inherit PermissionsMixin
class Account(AbstractUser):

    """Small extension of built-in User model

    Default User Role -> developer (is_manager=False)
    Default state of developer -> unassigned = True (has no task)
    Default task set for developer -> empty (unassigned)

    If 'is_manager' is True -> 'unassigned' and 'assigned_to'
        fields are not used.
    """

    username    = None
    email       = models.EmailField("email", unique=True)
    # Set user role, manager | developer
    is_manager  = models.BooleanField("manager", default=False)
    # Flag for 'developer' role, has no effect on 'manager' role
    # Specifies whether a developer has task assigned to him or not
    unassigned  = models.BooleanField("unassigned", default=True)
    # Task for 'developer' role, has no effect on 'manager' role
    # If developer is assigned, this field will store assigned task
    assigned_to = models.ForeignKey(Task, related_name="developers",
                    on_delete=models.SET_NULL, null=True,
                    blank=True)
    # Hidden fields:
    # managed_tasks -> related_name from Task model
    # writable_fields -> set(str), initialized on creation

    objects    = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # login field, django logic
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
        return f"{self.first_name}, {self.email}"

    def __repr__(self):
        # Used for ./manage.py commands
        return f"{self.id}, {self.email}" + \
        f"\n{self.is_manager = :}" +\
        f"\n{self.writable_fields}" +\
        f"\n{self.unassigned = :}" +\
        f"\n{self.assigned_to = :}\n"

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


all_models = [Task]


def assign_developer(sender, instance, created, **kwargs):
    """
    sender -> Model
    instance -> Model obj
    created -> bool
    update_fileds -> set of changed fields
    """

    print("assign_account() called")
    # print(sender)
    # print(dir(instance))
    print(instance.manager)
    print(type(instance.developers))
    if instance.developers == None:
        print("kek")
    print(instance.developers)
    print(created)
    # print(kwargs)

post_save.connect(assign_developer, sender=Task)

