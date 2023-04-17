from django.db import models
from users.models import userProfile

# Create your models here.


class Category(models.Model):
    category_name = models.TextField(null=False)
    category_code = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self', blank=True, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_name


class Region(models.Model):
    region_name = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.region_name


class Cities(models.Model):
    city_name = models.TextField(blank=False, null=False)
    Region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city_name


class Announcement(models.Model):
    class State(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin
        Draft = 'Draft', 'Draft'
        Moderate = "Moderate", "Moderate"
        Rejected = "Rejected", "Rejected"
        Active = 'Active', 'Active'

    name = models.TextField(blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    publication_date = models.DateField
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    cost = models.CharField(max_length=12, blank=False)
    user_id = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    views = models.IntegerField
    announce_state = models.CharField(max_length=20, choices=State.choices)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class announceModeration(models.Model):
    moderator = models.ForeignKey(
        userProfile, on_delete=models.SET_DEFAULT, default=1)
    announce_id = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    date_modertion = models.DateField
    publication = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
