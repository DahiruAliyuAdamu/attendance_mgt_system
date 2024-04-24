# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from attendance_app.models import Employee

class Account(AbstractUser):
    staff = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, related_name='staff')
    username = models.CharField(_('Username'), max_length=10, unique=True)
    password = models.CharField(_('Password'), max_length=16)

    def __str__(self) -> str:
        return f"{self.username}"