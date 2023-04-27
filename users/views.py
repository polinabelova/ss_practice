from django.views import generic
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm
from .choices import UserState
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .token import account_activation_token
from .models import User


# Create your views here.


def index(request):
    return render(request, "users/index.html")


def profile(request):
    return render(request, "users/profile.html")


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


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

            return redirect('/users/login/')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context
