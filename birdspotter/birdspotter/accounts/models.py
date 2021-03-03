import uuid

from django.contrib import messages
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from django.utils import timezone


class User(AbstractUser):
    """Custom user implementation
    Attributes:
        username (str): user specified username, used as unique identifier
    """
    username = models.CharField(max_length=30, unique=True)
    user_id = models.UUIDField(primary_key=False,
                               default=uuid.uuid4, editable=False, unique=True)

    def to_dict(self):
        """ Returns a dictionary representation of user information
        """
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def is_admin(self):
        """ Returns whether the current user is part of the admin group, or is a superuser
        """
        return self.groups.filter(name='Admin').exists() or self.is_superuser

    def make_active(self):
        """ Makes the current user active within the system
        """
        self.is_active = True
        self.save()

    def make_admin(self):
        """ Sets the is_staff flag when making a user an admin
        This allows a user of the admin group to reach the django admin site
        """
        self.is_staff = True
        self.save()


class GroupRequest(models.Model):
    """
    Role request model that allows admin approve or deny group requests

    Attributes:
        user (User): the user that is creating the request
        group (str): the group that the user is requesting
        submitted_date (datetime): the date and time that the request was created
        approved (boolean): whether the request is approved or not
        reviewed_by (User): the user that reviewed the request and either approved or denied the request
        notes (str < 2000 chars): notes that the requesting user can add to a request
    """
    groups = ['Admin', 'Privileged', 'Registered']

    GROUP_CHOICES = [(a, a) for a in groups]

    request_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='requesting_user')
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='Registered')
    submitted_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='approving_user')
    reviewed_date = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)

    def approve_request(self, request):
        """ Approves the group request and performs any other required actions
        based on the group request level
        """
        self.approved = True
        self.reviewed_by = request.user
        self.reviewed_date = timezone.now()
        try:
            permission_group = Group.objects.get(name=self.group)
            self.user.groups.add(permission_group)
            if self.group == 'Registered':
                user = User.objects.get(username=self.user.username)
                user.make_active()
            elif self.group == 'Admin':
                user.make_admin()
            messages.success(request, f'User {self.user} successfully added to {self.group}')
        except Group.DoesNotExist:
            messages.error(request, f'Permission group {self.group} does not exist')
        self.save()

    def deny_request(self, request):
        """ Denies the request and sets the review fields
        """
        self.approved = False
        self.reviewed_by = request.user
        self.reviewed_date = timezone.now()
        self.save()
