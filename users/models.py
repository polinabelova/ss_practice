from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class userProfile(models.Model):

    class State(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin  
        Active = 'Active', 'Active'
        Blocked = "Blocked", "Blocked"
        Waiting = "Waiting" ,"Waiting activation"
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{11}$")
    phoneNumber = models.CharField(
        validators=[phoneNumberRegex], max_length=12, unique=True)
    email_uniq = models.EmailField(blank=False, null=False, unique=True)
    call_time = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    state = models.CharField(max_length=7, blank=False, choices=State.choices)

    def __str__(self):
        return self.user.username



