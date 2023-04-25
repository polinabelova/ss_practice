from django.views import generic
from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

# Create your views here.


def index(request):
    return render(request, "users/index.html")


def profile(request):
    return render(request, "users/profile.html")


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
