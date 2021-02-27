from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import logging


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        try:
            default_group = Group.objects.get(name='Registered')
            instance.groups.add(default_group)
        except Exception:
            if not settings.TESTING:
                logging.critical('Groups have not been created and this application is not in DUBUG mode. Please run ./manage.py create_groups')
        instance.save()
