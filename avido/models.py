from django.db import models
from users.models import UserProfile
from .choices import *


class CommonInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(CommonInfo):
    name = models.CharField(max_length=30, null=True)
    code = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class Region(CommonInfo):
    name = models.CharField(max_length=40, blank=False, null=True)

    def __str__(self):
        return str(self.name)


class Cities(CommonInfo):
    name = models.CharField(max_length=30, blank=False, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)


class Announcement(CommonInfo):

    name = models.CharField(max_length=250, blank=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    date = models.DateField
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    cost = models.CharField(max_length=12, blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    views = models.IntegerField
    state = models.CharField(
        max_length=20, choices=AnnouncmentState.CHOICES, default=AnnouncmentState.draft)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)

    def __str__(self):
        return str(self.name)


class AnnounceModeration(CommonInfo):
    moderator = models.ForeignKey(
        UserProfile, on_delete=models.SET_DEFAULT, default=1)
    announce = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    date = models.DateField
    publication = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
