from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail


from .models import GroupRequest
from birdspotter.utils import GROUPS

import logging


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user(instance, created, **kwargs): # noqa
    if created:
        try:
            default_group = Group.objects.get(name=GROUPS['default'])
            instance.groups.add(default_group)
        except Group.DoesNotExist:
            if not settings.TESTING:
                logging.critical('Groups have not been created and this application is not in DEBUG mode. '
                                 'Please run ./manage.py create_groups')
        instance.save()

@receiver(post_save, sender=GroupRequest)
def send_email_on_group_request(instance, created, **kwargs): # noqa
    if created:
        # send email to admin
        send_mail(subject=f'{instance.user} requests {instance.group} permissions',
                  message=f'Notes provided:\n{instance.notes}',
                  from_email='system@birdspotter.net',
                  recipient_list=['test@test.com'])
