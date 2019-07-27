

from django.db import models
from datetime import date


# Create your models here.
class ItemGroup(models.Model):
    deadline = models.DateField(default = date.today)
    owner = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)
    
class ToDoItem(models.Model):
    item = models.CharField(max_length=200)
    deadline = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return self.item + ' | ' + str(self.completed)

class WishList(models.Model):
    item = models.CharField(max_length = 200)
    points = models.IntegerField(default = 0)
    link = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)

    def __str__(self):
        return self.item + "|" + str(self.points)



