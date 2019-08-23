

from django.db import models
from datetime import date
'''
class ItemGroup(models.Model):
    deadline = models.DateField(default = date.today)
    owner = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)

    def __str__(self):
        return str(self.deadline) + '|' + self.owner.username
'''  
class ToDoItem(models.Model):
    item = models.CharField(max_length=200)
    ddl_date = models.DateField(default = date.today)
    #deadline = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    points = models.IntegerField(default=100)
    completed = models.BooleanField(default = False)
    owner = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)

    def __str__(self):
        return self.item + ' | ' + str(self.completed)

class WishList(models.Model):
    item = models.CharField(max_length = 200)
    points = models.IntegerField(default = 0)
    link = models.CharField(max_length = 200)
    description = models.CharField(max_length = 1000)
    owner = models.ForeignKey('authentication.CustomUser', on_delete = models.CASCADE)

    def __str__(self):
        return self.item + "|" + str(self.points)



