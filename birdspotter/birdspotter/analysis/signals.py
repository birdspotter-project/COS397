from django_mailbox.signals import message_received
from django.dispatch import receiver
from .scripts.update_job import handle_update
from django.conf import settings
@receiver(message_received)
def handle_mail(sender, message, **args): # noqa
    if sender == settings.EMAIL_NOTIF_ADDR:
        handle_update(message)