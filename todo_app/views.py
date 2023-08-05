from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import ToDoItem, ToDoList
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView,LogoutView
from todo_app.forms import SignUpForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



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
@method_decorator(login_required, name='dispatch')
class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

@method_decorator(login_required, name='dispatch')
class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

@method_decorator(login_required, name='dispatch')
class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def form_valid(self, form):
        # Check if a ToDoList with the provided title already exists
        title = form.cleaned_data["title"]
        if ToDoList.objects.filter(title=title).exists():
            # Display an error message to the user
            messages.error(
                self.request, f"A list with the name '{title}' already exists."
            )
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["title"] = "Add a new list"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.id])


@method_decorator(login_required, name='dispatch')
class ItemCreate(CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = f"Add a New Item to {todo_list.title}"
        return context

    def get_success_url(self) -> str:
        return reverse("list", args=[self.object.todo_list_id])

@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = f"Update {self.object.title}"
        return context

    def get_success_url(self) -> str:
        return reverse("list", args=[self.object.todo_list_id])


@method_decorator(login_required, name='dispatch')
class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")



@method_decorator(login_required, name='dispatch')
class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self, **kwargs):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
