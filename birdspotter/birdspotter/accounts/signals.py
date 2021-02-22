from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name='Registered')
        instance.groups.add(default_group)
