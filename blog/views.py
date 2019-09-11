from django.shortcuts import render,redirect
from . import models
from .forms import ArticleForm
from django.contrib import messages

# Create your views here.

def articles_list(request):
    articles = models.Article.objects.all()
    return render(request, 'articles_list.html',{"articles":articles})

def add_article(request):
    if not request.user.is_authenticated:
        messages.warning(request,("You are not logged in!"))
        return redirect(articles_list)
    user = request.user
    if request.method == 'POST':
        form = ArticleForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            item = form.save(commit = False)
            # processing category
            if models.Category.objects.filter(name = request.POST['category']).exists():
                category = models.Category.objects.get(name = request.POST['category'])
            else:
                category = models.Category.objects.create(name = request.POST['category'])
                category.save()
            item.category = category
            item.author = user
            item.save()
            #processing tags
            tags = request.POST['tags'].strip().split()
            for tag in tags:
                if models.Tag.objects.filter(name = tag).exists():
                    tag_object = models.Tag.objects.get(name = tag)
                else:
                    tag_object = models.Tag.objects.create(name = tag)
                    tag_object.save()
                item.tags.add(tag_object)
            
            item.save()
            return redirect(articles_list)
        else:
            messages.warning(request,("Your input is not valid:"))
            return render(request, 'add_article.html',{"errors":form.errors, 'forms':form})
    else:
        return render(request, 'add_article.html',{})
            
            

