from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from . import models
from .forms import SignUpForm


def login_user(request):
    # if the login button clicked
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # if the user exist
        if user is not None:
            login(request, user)
            # TODO rewrite to profile or home page
            return redirect('profile')  # redirect by hardcoded URL
        else:
            messages.warning(request, ('Incorrect username or password'))
            return redirect('login-user')  # redirect by URL name
    else:
        return render(request, 'auth/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out...'))
    return redirect('home')


def profile(request):
    return render(request, 'auth/profile.html', {})


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ("Successfully Saved!"))
                return redirect('profile')
            else:
                messages.warning(request,('Your form has errors'))
                return render(request,'auth/edit_profile.html',{'form':form})
        form = UserChangeForm(instance = request.user)

        context = {'form': form}
        return render(request,'auth/edit_profile.html',context)
    else:
        messages.warning(request,('Your are not logged in!'))
        return redirect('login_user')

def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request,('Already registered!'))
        return redirect('profile')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request, ("Registered!"))
            return redirect('home')
        else:
            messages.warning(request,('Your form has errors'))
            return render(request,'auth/register.html',{'form':form})

    form = SignUpForm()

    context = {'form': form}
    return render(request,'auth/register.html',context)


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user) #stop logout
                messages.success(request, ("Successfully Saved!"))
                return redirect('profile')
            else:
                messages.warning(request,('Your form has errors'))
                return render(request,'auth/change_password.html',{'form':form})
        form = PasswordChangeForm(user = request.user)

        context = {'form': form}
        return render(request,'auth/change_password.html',context)
    else:
        messages.warning(request,('Your are not logged in!'))
        return redirect('login_user')
