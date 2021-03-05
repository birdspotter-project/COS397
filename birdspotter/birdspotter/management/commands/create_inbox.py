from django_mailbox.models import Mailbox 
from django.conf import settings 
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates default inbox based on settings.py'
    def handle(self, *args, **options):
        if(settings.PROD_EMAIL.lower() == "true" and Mailbox.objects.get(name="default") is None):
            mbx = Mailbox(active=True, name="default",uri=settings.IMAP_URI,from_email=settings.EMAIL_HOST_USER)
            mbx.save()