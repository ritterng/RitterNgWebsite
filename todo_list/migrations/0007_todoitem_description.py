# Generated by Django 2.2.4 on 2019-09-05 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_list', '0006_auto_20190823_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
