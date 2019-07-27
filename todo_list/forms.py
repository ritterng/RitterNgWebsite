from django import forms
from .models import ToDoItem, WishList, ItemGroup

class ListForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ["item","points","completed"]
    

class WishForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = ["item", "points", "link", "description"]