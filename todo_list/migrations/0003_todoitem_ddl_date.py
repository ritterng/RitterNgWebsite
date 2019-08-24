# Generated by Django 2.1.10 on 2019-08-22 07:12

import datetime
from django.db import migrations, models
def add_ddl_date(apps, scheme_editor):
    items = apps.get_model("todo_list", "todoitem")
    for item in items.objects.all().iterator():
        item.ddl_date = item.deadline.deadline
        item.save()

def reverse_add_ddl_date(apps, scheme_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0002_todoitem_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='ddl_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.RunPython(add_ddl_date, reverse_add_ddl_date),
    ]