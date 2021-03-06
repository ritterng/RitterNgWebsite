# Generated by Django 2.1.10 on 2019-08-22 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def add_owner(apps, schema_editor):
    items = apps.get_model('todo_list','todoitem')
    for item in items.objects.all().iterator():
        item.owner = item.deadline.owner
        item.save()
    
def revers_add_owner(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(add_owner,revers_add_owner)
    ]
