#!/usr/bin/env python3

from django.core.management.base import (
    BaseCommand,
    CommandError)
from django.db.utils import IntegrityError
from tasks.models import Account

class Command(BaseCommand):

    help = "Delete unworthy!"

    def add_arguments(self, parser):
        parser.add_argument("ids", nargs="*", type=int)
        parser.add_argument("-a", "--all", action="store_true")

    def handle(self, *args, **kwargs):
        if kwargs["all"] == True:
            all_users = Account.objects.all()
            amt = len(all_users)
            for user in all_users:
                user.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {amt} Users!"))
            return
        else:
            if not len(kwargs["ids"]):
                raise CommandError("Supply at least one 'id'!")
            amt = 0
            for i in kwargs["ids"]:
                try:
                    user = Account.objects.get(pk=i)
                    user.delete()
                    amt += 1
                except Account.DoesNotExist:
                    raise CommandError(f"Account {i} does not exist!") 
            self.stdout.write(self.style.SUCCESS(f"Deleted {amt} Users!"))
