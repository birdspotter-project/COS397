from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from .models import GroupRequest

import logging


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user(instance, created, **kwargs): # noqa
    """ When a user is saved, make that user inactive until the admin approves
    the request.

    Attributes:
        instance (User): the user instance that was saved to the database
        created (boolean): flag for if the save was successful
    """
    if created:
        """superusers can be ignored because they do not go through the 
        normal sign up flow
        """
        if not instance.is_superuser:
            instance.is_active = False
        try:
            default_group = Group.objects.get(name='Registered')
            instance.groups.add(default_group)
        except Group.DoesNotExist:
            if not settings.TESTING:
                logging.critical('Groups have not been created and this application is not in DEBUG mode. '
                                 'Please run ./manage.py create_groups')
        instance.save()

@receiver(post_save, sender=GroupRequest)
def send_email_on_group_request(instance, created, **kwargs): # noqa
    """ Send an email to the main admin alerting them when someone requests
    a permissions group (including the transition from Public -> Registered)
    """
    if created:
        send_mail(subject=f'{instance.user} requests {instance.group} permissions',
                  message=f'Notes provided:\n{instance.notes}',
                  from_email='system@birdspotter.net',
                  recipient_list=['test@test.com'])
