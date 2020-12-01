from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user implementation

    Attributes:
        username (str): user specified username, used as unique identifier
    """

    username = models.CharField(max_length=30, unique=True)
