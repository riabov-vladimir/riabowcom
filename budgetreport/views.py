from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView

from django.contrib import auth

def auth_view(request):

    # here you get the post request username and password
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    # authentication of the user, to check if it active or None
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            # this is where the user login actually happens, before this the user
            # is not logged in.
            auth.login(request, user)

            return ...

    else :
        return HttpResponseRedirect("Invalid username or password")
