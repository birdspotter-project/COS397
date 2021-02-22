from django_mailbox.signals import message_received
from django.dispatch import receiver

@receiver(message_received)
def dance_jig(sender, message, **args):
    print("I just recieved a message titled %s from a mailbox named %s, titled to %s" % (message.subject, message.mailbox.name, sender ) )