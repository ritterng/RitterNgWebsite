# Generated by Django 2.1.10 on 2019-08-22 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0003_todoitem_ddl_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemgroup',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='todoitem',
            name='deadline',
        ),
        migrations.DeleteModel(
            name='ItemGroup',
        ),
    ]
