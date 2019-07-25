# Generated by Django 2.1.10 on 2019-07-25 03:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('deadline', models.DateField(default=datetime.date.today)),
                ('points', models.IntegerField(default=100)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
