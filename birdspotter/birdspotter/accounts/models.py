from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

import uuid


class User(AbstractUser):
    """Custom user implementation
    Attributes:
        username (str): user specified username, used as unique identifier
    """
    username = models.CharField(max_length=30, unique=True)
    user_id = models.UUIDField(primary_key=False,
                               default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    def to_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
