from django.contrib import admin
from .models import *
admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Region)
admin.site.register(Cities)
admin.site.register(announceModeration)
# Register your models here.
