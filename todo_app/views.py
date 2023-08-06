from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import ToDoItem, ToDoList
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime as dt
from django.shortcuts import redirect, get_object_or_404


# Create your views here.


@method_decorator(login_required, name="dispatch")
class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


@method_decorator(login_required, name="dispatch")
class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        list_id = self.kwargs["list_id"]
        return self.model.objects.filter(todo_list_id=list_id, owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(
            id=self.kwargs["list_id"], owner=self.request.user
        )
        context["todo_list"] = todo_list
        return context


@method_decorator(login_required, name="dispatch")
class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new list"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.id])


@method_decorator(login_required, name="dispatch")
class ItemCreate(CreateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(
            id=self.kwargs["list_id"], owner=self.request.user
        )
        context["todo_list"] = todo_list
        context["title"] = f"Add a New Item to {todo_list.title}"
        return context

    def get_success_url(self) -> str:
        return reverse("list", args=[self.object.todo_list_id])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = ["todo_list", "title", "description", "due_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todo_list = self.object.todo_list
        if self.object.owner != self.request.user:
            return redirect("index")
        context["title"] = f"Update {self.object.title}"
        return context

    def get_success_url(self) -> str:
        return reverse("list", args=[self.object.todo_list_id])


@method_decorator(login_required, name="dispatch")
class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


@method_decorator(login_required, name="dispatch")
class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self, **kwargs):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context


@login_required
def mark_item_done(request, list_id, item_id):
    todo_item = get_object_or_404(ToDoItem, todo_list_id=list_id, id=item_id)
    if todo_item.owner != request.user:
        return redirect("index")
    todo_item.is_completed = True
    todo_item.completed_date = dt.datetime.now()
    todo_item.save()
    return redirect("list", list_id)
