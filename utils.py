#!/usr/bin/env python3

"""Only for import in django shell"""

def create_users():
    from tasks.models import Developer, Manager

    DEVS = ("Brian Kernighan", "Ken Thompson", "Alan Perlis")
    MANS = ("Henry Ford", "Elon Musk")

    for d in DEVS:
        Developer(name=d).save()
    for m in MANS:
        Manager(name=m).save()


def list_users():
    from tasks.models import Developer, Manager, Task

    DEVS = ("Brian Kernighan", "Ken Thompson", "Alan Perlis")
    MANS = ("Henry Ford", "Elon Musk")
    print("Developers:")
    for e in Developer.objects.all():
        print(f"\t{e.id} {e.name}")
    print("Managers:")
    for e in Manager.objects.all():
        print(f"\t{e.id} {e.name}")


def list_tasks():
    from tasks.models import Task
    for e in Task.objects.all():
        print(e)

def reimport():
    from sys import modules
    from importlib import reload
    return reload(modules[__name__])
