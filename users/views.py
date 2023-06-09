from django.views import generic, View
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import account_activation_token
from .models import User
from .choices import UserState
from .forms import RegisterForm, LoginForm, UserPasswordResetForm


class IndexView(TemplateView):
    template_name = "users/index.html"


class ProfileView(TemplateView):
    template_name = "users/profile.html"


class UserAccountView(TemplateView):
    template_name = 'users/user_account.html'


class ModeratorAccountView(TemplateView):
    template_name = 'users/moderator_account.html'


class AdminAccountView(TemplateView):
    template_name = 'users/admin_account.html'


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_redirect_url(self):
        redirect_url = super().get_redirect_url()
        user = self.request.user
        if user.groups.filter(name='User').exists():
            redirect_url = ('/users/user-account')
        elif user.groups.filter(name='Moderator').exists():
            redirect_url = ('/users/moderator-account')
        elif user.groups.filter(name='Admin').exists():
            redirect_url = ('/users/admin-account')
        # временно
        else:
            redirect_url = ('/users')
        return redirect_url


class LogoutView(auth_views.LogoutView):
    pass


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('/profile')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={
                                      'uidb64': uid, 'token': token})
        current_site = 'http://localhost:8000'
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'polinabelova404@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('email_confirmation_sent')

# Подтверждение почты при авторизации
# Проверка пользователя по токену

class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.state = UserState.active
            user.save()
            user.groups.add(Group.objects.get(name='User'))

            return redirect('/users/login/')
        else:
            return redirect('email_confirmation_failed')


# Успешная отправка письма для активации на почту
class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'


# Ошибка проверки пользователя по токену
class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'


# Восстановление пароля
class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserPasswordResetForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('login')
    subject_template_name = 'users/subject_password_reset_email.txt'
    email_template_name = 'users/acc_password_reset_email.html'


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = SetPasswordForm
    template_name = 'users/user_password_set.html'
    success_url = reverse_lazy('login')
