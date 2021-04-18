from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import logging


def send_email_to_admins(subject, message, from_email=""):
    User = get_user_model()
    admin_emails = [a.email for a in User.objects.filter(is_staff=True)]
    if not admin_emails:
        logging.error('The application has no admins')
    else:
        return send_mail(subject, message, from_email, admin_emails) == 1
    return False