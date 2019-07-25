from django.db import models
from datetime import date


# Create your models here.

class List(models.Model):
    item = models.CharField(max_length=200)
    deadline = models.DateField( default=date.today)
    points = models.IntegerField(default=100)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.item + ' | ' + str(self.completed)