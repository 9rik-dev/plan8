#!/usr/bin/env python3

from .models import Account
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,)
from django.forms import ModelForm


import logging

logger = logging.getLogger(__name__)

class LoggingMixin(object):
    def add_error(self, field, error):
        if field:
            print(f"Form error on field {field = :}: {error = :}")
        else:
            print('Form error: %s', error)
        super().add_error(field, error)


class AccountCreationForm(LoggingMixin, ModelForm):
    class Meta:
        model = Account
        fields = ('email',)


class AccountChangeForm(LoggingMixin, ModelForm):

    class Meta:
        model = Account
        fields = ('email',)
