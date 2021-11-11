#!/usr/bin/env python3
from django.db import migrations


def create_test_tasks(apps, schema_editor):

    Task = apps.get_model("tasks", "Task")

    Task(title="We need rockets",
        description="Rewrite Apollo 11 guidance system in Brainfuck language",
        status=0, prior=3).save()
    Task(title="Web Dev",
        description="Write a static website in AWK",
        status=0, prior=1).save()
    Task(title="Marketing",
        description="Simulate a perfect hill for our Ford Model T to slither down, using neural nets.",
        status=0, prior=2).save()


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operation = [
        migrations.RunPython(create_test_tasks),
    ]
 
