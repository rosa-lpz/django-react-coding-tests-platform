# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # You can add additional fields here if needed
    # Example: 
    # birthday = models.DateField(null=True, blank=True)

    # Custom related names for the groups and permissions
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the reverse related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Change the reverse related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    # Other custom fields can go here if necessary