from django.shortcuts import render
from . import models

# Create your views here.

def articles_list(request):
    articles = models.Article.objects.all()
    return render(request, 'articles_list.html',{"articles":articles})
