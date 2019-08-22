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

    if request.method == 'POST':
        form = ListForm(request.POST or None)
        user = request.user


        if form.is_valid():
            item = form.save()
            '''
            item = form.save(commit=False)
            
            date = request.POST['deadline']
            try:
                #TODO update
                group = ItemGroup.objects.get(deadline = date, owner = user)
            except:
                print('fail to retret')
                #TODO update
                group = ItemGroup(deadline = date, owner = user)
                group.save()
            item.deadline = group
            item.save()
            '''
            all_items = ToDoItem.objects.all
            messages.success(request, ('Item Has Been Added To List!'))
            return render(request, 'todo/home.html', {'all_items': all_items})
        else:
            #all_items = ToDoItem.objects.all
            #messages.warning(request, ('Item cannot be empty!'))
            messages.warning(request, (form.errors))
            return render(request, 'todo/home.html', {'all_items': all_items})

    else:
        all_items = ToDoItem.objects.all
        return render(request, 'todo/home.html', {'all_items': all_items})

@login_required
def delete(request, list_id):
    item = ToDoItem.objects.get(pk=list_id)
    item.delete()
    messages.success(request, ("Item has been Deleted"))
    return redirect('home')

@login_required
def cross_off(request, list_id):
    item = ToDoItem.objects.get(pk=list_id)
    user = UserModel.objects.get(pk = request.user.id)
    user.points += item.points
    user.save()
    item.completed = True
    item.save()
    return redirect('home')

@login_required
def uncross(request, list_id):
    item = ToDoItem.objects.get(pk=list_id)
    user = UserModel.objects.get(pk = request.user.id)
    user.points -= item.points
    user.save()
    item.completed = False
    item.save()
    return redirect('home')

@login_required
def edit(request, list_id):
    if request.method == 'POST':
        item = ToDoItem.objects.get(pk=list_id)
        form = ListForm(request.POST or None, instance=item)  
        user = request.user      
        if form.is_valid():
            item = form.save()
            '''
            date = request.POST['deadline']
            try:
                #TODO Update Item Group
                group = ItemGroup.objects.get(deadline = date, owner = user)
            except:
                print('fail to retret')
                #TODO Update Item Group
                group = ItemGroup(deadline = date, owner = user)
                group.save()
            item.deadline = group
            item.save()
            '''
            messages.success(request, ('Item Has Been Edited!'))
            return redirect('home')

    else:
        item = ToDoItem.objects.get(pk=list_id)
        return render(request, 'todo/edit.html', {'item': item})
        
def wish_list_home(request):
    if not request.user.is_authenticated:
        messages.warning(request,('You are not logged in!'))
        return redirect('index')
    if request.method == 'POST':
        form = WishForm(request.POST or None)

        if form.is_valid:
            form.save()
            items = WishList.objects.all()
            messages.success(request,("Wish has been added!"))
            return render(request, "wish/wish-list.html",{'items':items})
        else:
            items = WishList.objects.all()
            messages.warning(request,("Wish form has error(s)"))
            return render(request, "wish/wish-list.html",{'items':items})
    items = WishList.objects.all()
    return render(request, "wish/wish-list.html",{'items':items})

