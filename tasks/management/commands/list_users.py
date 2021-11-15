#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from tasks.models import Account

class Command(BaseCommand):

    help = "Output all Users to stdout."

    def handle(self, *args, **kwargs):
        for user in Account.objects.all():
            self.stdout.write(self.style.SUCCESS(repr(user)))
