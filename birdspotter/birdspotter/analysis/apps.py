from django.apps import AppConfig

class AnalysisConfig(AppConfig):
    name = 'birdspotter.analysis'
    def ready(self):
        from .signals import handle_mail # noqa
        from django_mailbox.models import Mailbox # noqa
        from django.conf import settings # noqa
        if(settings.PROD_EMAIL.lower() == "true" and Mailbox.objects.get(name="default") is None):
            mbx = Mailbox(active=True, name="default",uri=settings.IMAP_URI,from_email=settings.EMAIL_HOST_USER)
            mbx.save()