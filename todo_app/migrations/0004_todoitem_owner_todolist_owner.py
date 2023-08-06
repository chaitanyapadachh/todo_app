# Generated by Django 4.2.4 on 2023-08-06 06:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_app', '0003_alter_todoitem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='owner',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, related_name='todo_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todolist',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='todo_lists', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]