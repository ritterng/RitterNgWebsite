from django.shortcuts import render, redirect
from .models import ToDoItem, WishList
from .forms import ListForm, WishForm
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.decorators import login_required

UserModel = apps.get_model('authentication','CustomUser')

def index(request):
    return render(request, 'index.html',{})


def home(request):
    if not request.user.is_authenticated:
        messages.warning(request,("You are not logged in!"))
        return redirect(index)
    user = request.user
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            item = form.save(commit = False)
            item.owner = user
            item.save()
            all_items = ToDoItem.objects.filter(owner = user)
            messages.success(request, ('Item Has Been Added To List!'))
            return render(request, 'todo/home.html', {'all_items': all_items})
        else:
            all_items = ToDoItem.objects.all
            messages.warning(request, ('Item cannot be empty!'))
            #messages.warning(request, (form.errors))
            return render(request, 'todo/home.html', {'all_items': all_items})

    else:
        all_items = ToDoItem.objects.filter(owner = user)
        return render(request, 'todo/home.html', {'all_items': all_items})

@login_required
def delete(request, list_id):
    if not ToDoItem.objects.filter(id = list_id).exists():
        messages.warning(request,("Item does not exist!"))
        return redirect('home')
    item = ToDoItem.objects.get(pk=list_id)
    user = request.user
    if item.owner != user:
        messages.warning(request,("You don't have permissions to modify this item!"))
        return redirect('home')
    item.delete()
    messages.success(request, ("Item has been Deleted"))
    return redirect('home')

@login_required
def cross_off(request, list_id):
    if not ToDoItem.objects.filter(id = list_id).exists():
        messages.warning(request,("Item does not exist!"))
        return redirect('home')
    item = ToDoItem.objects.get(pk=list_id)
    if item.owner != request.user:
        messages.warning(request,("You don't have permissions to modify this item!"))
        return redirect('home')      
    user = UserModel.objects.get(pk = request.user.id)
    user.points += item.points
    user.save()
    item.completed = True
    item.save()
    return redirect('home')

@login_required
def uncross(request, list_id):
    if not ToDoItem.objects.filter(id = list_id).exists():
        messages.warning(request,("Item does not exist!"))
        return redirect('home')
    item = ToDoItem.objects.get(pk=list_id)
    if item.owner != request.user:
        messages.warning(request,("You don't have permissions to modify this item!"))
        return redirect('home') 
    user = UserModel.objects.get(pk = request.user.id)
    user.points -= item.points
    user.save()
    item.completed = False
    item.save()
    return redirect('home')

@login_required
def edit(request, list_id):
    if request.method == 'POST':
        if not ToDoItem.objects.filter(id = list_id).exists():
            messages.warning(request,("Item does not exist!"))
            return redirect('home')
        item = ToDoItem.objects.get(pk=list_id)
        user = request.user 
        if item.owner != user:
            messages.warning(request,("You don't have permissions to modify this item!"))
            return redirect('home')
        form = ListForm(request.POST or None, instance=item)     
        if form.is_valid():
            item = form.save(commit = False)
            item.owner = user
            item.save()
            messages.success(request, ('Item Has Been Edited!'))
            return redirect('home')
        else:
            message.warning(request,("failed"))
            return redirect('home')

    else:
        item = ToDoItem.objects.get(pk=list_id)
        return render(request, 'todo/edit.html', {'item': item})
        
def wish_list_home(request):
    if not request.user.is_authenticated:
        messages.warning(request,('You are not logged in!'))
        return redirect('index')
    user = request.user
    if request.method == 'POST':
        form = WishForm(request.POST or None)

        if form.is_valid:
            item = form.save(commit=False)
            item.owner = user
            item.save()
            items = WishList.objects.all()
            messages.success(request,("Wish has been added!"))
            return render(request, "wish/wish-list.html",{'items':items})
        else:
            items = WishList.objects.all()
            messages.warning(request,("Wish form has error(s)"))
            return render(request, "wish/wish-list.html",{'items':items})
    items = WishList.objects.all()
    return render(request, "wish/wish-list.html",{'items':items})



