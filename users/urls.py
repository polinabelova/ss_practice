from django.urls import path
from .views import *
urlpatterns = [

    path('', index, name="users"),
    path('profile', profile, name="profile"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(),
         name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         UserConfirmEmailView.as_view(), name='confirm_email'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(),
         name='email_confirmation_failed'),

]
