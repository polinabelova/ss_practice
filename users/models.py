from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .choices import *


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(CommonInfo):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    PhoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{11}$")
    phone = models.CharField(
        validators=[PhoneNumberRegex], max_length=12, unique=True)
    email_uniq = models.EmailField(blank=False, null=False, unique=True)
    call_time = models.TextField(blank=True)
    state = models.CharField(max_length=7, blank=False,
                             choices=UserState.CHOICES)

    def __str__(self):
        return self.user.username
