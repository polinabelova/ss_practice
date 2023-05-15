from django.urls import path
from .views import *
urlpatterns = [

    path('', IndexView.as_view(), name="users"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('user-account/', UserAccountView.as_view(), name='user_account'),
    path('moderator-account/', ModeratorAccountView.as_view(),
         name='moderator_account'),
    path('admin-account/', AdminAccountView.as_view(), name='admin_account'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(),
         name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         UserConfirmEmailView.as_view(), name='confirm_email'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(),
         name='email_confirmation_failed'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
