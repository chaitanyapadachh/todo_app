from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class ToDoList(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def get_abolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=one_week_hence)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("item-update", args=[str(self.todo_list.id), str(self.id)])

    def __str__(self):
        return f"{self.title}: due {self.due_date.strftime('%d %b %Y %H:%M')}"

    class Meta:
        ordering = ["is_completed","due_date"]
