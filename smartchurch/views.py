from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from .forms import *
from .models import *


# Create your views here.

# @unauthenticated_user
def login_view(request):
    # create an instance the UserLoginForm in the form.py passing in request.Post or None as an argument
    form = UserLoginForm(request.POST or None)
    if form.is_valid():  # if the data passed to the UserLoginForm in the form.py is passes all the clean data methods
        # get the username form the already clearned data in UserLoginForm class in the form.py and store it into a varible called username
        username = form.cleaned_data.get('username')
        # get the password form the already clearned data in UserLoginForm class in the form.py and store it into a varible called password
        password = form.cleaned_data.get('password')
        # re-authenticate the username and password and store it into variable called user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('accounts:dashboard')

        else:
            messages.info(request, 'Username or Password is incorrect')
            # redirect the user to the managers user homepage which is yet to be added
            return redirect("log")

    context = {
        'form': form,  # context is the form itself
    }
    # render login page with the request and context
    return render(request, "church/login.html", context)


# a function to log out a user
def logout_request(request):
    logout(request)  # passout the request as an argument to the logout() function
    return redirect("log")  # redirect to the login page


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            pro = request.user.id
            cc = Profile.objects.get(user=pro)
            cc.is_new = False
            cc.save()
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('log')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })
