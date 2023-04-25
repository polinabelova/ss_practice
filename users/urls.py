from django.urls import path
from .views import *
urlpatterns = [

    path('', index, name="users"),
    path('profile', profile, name="profile"),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    
    
]
