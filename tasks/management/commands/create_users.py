#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from tasks.models import Account


FNAMES = ("James", "Robert", "John", "Michael","William",
    "David", "Richard", "Joseph", "Thomas", "Charles",
    "Christopher", "Daniel", "Matthew", "Anthony",
    "Mark", "Donald", "Steven", "Paul", "Andrew",
    "Joshua", "Kenneth", "Kevin", "Brian", "George",
    "Edward", "Ronald", "Timothy", "Jason", "Jeffrey",
    "Ryan", "Jacob", "Gary", "Nicholas", "Eric",
    "Jonathan", "Stephen", "Larry", "Justin", "Scott",
    "Brandon",)

LNAMES = ("Smith", "Johnson", "Williams", "Jones", "Brown",
    "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Garcia",
    "Martinez", "Robinson", "Clark", "Rodriguez",
    "Lewis", "Lee", "Walker", "Hall", "Allen",
    "Young", "Hernandez", "King", "Wright", "Lopez",
    "Hill", "Scott", "Green", "Adams", "Baker",
    "Gonzalez", "Turner", "Phillips",)

SUFF = "@test.com"
PASSWORD = "12345"

class Command(BaseCommand):

    help = "Creates set of random Users for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument("total", default=10, nargs="?", type=int)

    def handle(self, *args, **kwargs):
        total = kwargs["total"]

        if total >= len(FNAMES):
            self.stdout.write(self.style.NOTICE(f"Can reate at least 10, at most {len(FNAMES) - 1} Users!"))
            return

        if total < 10:
            self.stdout.write(self.style.WARNING(f"Creating 10 Users..."))
            total = 10

        try:

            Account.objects.create_superuser(email="admin" + SUFF,
                password="admin")
            self.stdout.write(self.style.SUCCESS(f"Created admin!"))

            m = int(total * 0.3)
            for i in range(m):
                Account.objects.create_user(email=FNAMES[i].lower() + SUFF,
                    password=PASSWORD, first_name=FNAMES[i],
                    last_name=LNAMES[i], is_manager=True)
            self.stdout.write(self.style.SUCCESS(f"Created {m} Managers!"))

            for i in range(m, total- 1):
                Account.objects.create_user(email=FNAMES[i].lower() + SUFF,
                    password=PASSWORD, first_name=FNAMES[i],
                    last_name=LNAMES[i])
            self.stdout.write(self.style.SUCCESS(f"Created {total - 1 - m} Developers!"))


        except IntegrityError:
            self.stdout.write(self.style.NOTICE(f"Set of Users already exists!"))
            self.stdout.write(self.style.WARNING(f"Use './manage.py delete_users' before runinng this command!"))
