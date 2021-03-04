import uuid

from django.contrib import messages
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from django.utils import timezone
from birdspotter.utils import GROUPS


class User(AbstractUser):
    """Custom user implementation
    Attributes:
        username (str): user specified username, used as unique identifier
    """
    username = models.CharField(max_length=30, unique=True)
    user_id = models.UUIDField(primary_key=False,
                               default=uuid.uuid4, editable=False, unique=True)

    def to_dict(self):
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def is_admin(self):
        return self.groups.filter(name=GROUPS['admin']).exists() or self.is_superuser

    def make_active(self):
        self.is_active = True
        self.save()

    def make_admin(self):
        self.is_staff = True
        self.save()


class GroupRequest(models.Model):
    """
    Role request model that allows admin approve or deny group requests
    """
    groups = ['Admin', 'Privileged', 'Registered']

    GROUP_CHOICES = [(a, a) for a in groups]

    request_id = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name='requesting_user')
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default=GROUPS['default'])
    submitted_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='approving_user')
    reviewed_date = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)

    def approve_request(self, request):
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
        self.approved = False
        self.reviewed_by = request.user
        self.reviewed_date = timezone.now()
        self.save()
