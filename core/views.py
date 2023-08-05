from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from core.forms import SignUpForm,LoginForm

from django.views.generic import  CreateView
# Create your views here.
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "todo_app/login.html"
    success_url = reverse_lazy("index")
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'todo_app/signup.html'