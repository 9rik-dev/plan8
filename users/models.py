from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
    )
# from django.contrib.auth.validators import UnicodeUsernameValidator

class AccountManager(BaseUserManager):
    """Most of this copied from django source"""
    use_in_migrations = True


    def create_user(self, email, password=None, **fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError("Email is mandatory")
        user = self.model(email=self.normalize_email(email), **fields)

        # user.password = make_password(password)
        user.set_password(password)  # what is the difference with above
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    """Almost identical to django source, except username is not used"""

    email           = models.EmailField("email", unique=True)
    first_name      = models.CharField("first name", max_length=150)
    last_name       = models.CharField("last name", max_length=150)

    is_active       = models.BooleanField("active", default=True)
    is_staff        = models.BooleanField("staff", default=False)
    is_admin        = models.BooleanField("admin", default=False)
    is_superuser    = models.BooleanField("superuser", default=False)

    date_joined     = models.DateTimeField("join date", auto_now_add=True)
    last_login      = models.DateTimeField("last login", auto_now=True)

    objects = AccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # login field
    REQUIRED_FIELDS = ["first_name", "last_name"]  # email already required

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"



    # Stolen from django source
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """Send an email to this user."""
    #     send_mail(subject, message, from_email, [self.email], **kwargs)
