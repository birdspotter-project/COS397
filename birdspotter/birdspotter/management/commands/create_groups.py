import logging

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

PERMISSIONS = {
    "Admin": {
        # django permissions
        "log entry": ["add", "delete", "change", "view"],
        "group": ["add", "delete", "change", "view"],
        "permission": ["add", "delete", "change", "view"],
        "user": ["add", "delete", "change", "view"],
        "content type": ["add", "delete", "change", "view"],
        "session": ["add", "delete", "change", "view"],

        # Birdspotter specific permissions
        "dataset": ["add", "delete", "change", "view", "export"],
        "shapefile": ["add", "delete", "change", "view"],
        "image": ["add", "delete", "change", "view"],
        "raw data": ["add", "delete", "change", "view"],
    },
    "Privileged": {
        "dataset": ["add", "delete", "change", "view", "export"],
    },
    "Registered": {
        "dataset": ["view", "export"],
    },
    "Public": {
        "dataset": ["view"],
    },
}


class Command(BaseCommand):
    help = 'Creates groups and permissions for the application'

    def handle(self, *args, **options):
        for group in PERMISSIONS:
            new_group, _ = Group.objects.get_or_create(name=group)
            for model in PERMISSIONS[group]:
                for permission in PERMISSIONS[group][model]:
                    dj_str = 'Can {} {}'.format(permission, model)
                    try:
                        model_perm = Permission.objects.get(name=dj_str)
                    except Permission.DoesNotExist:
                        logging.warning("Permission %s not found", dj_str)
                        continue
                    new_group.permissions.add(model_perm)
