from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# just login would override the contrib.auth.login funct,
# https://stackoverflow.com/questions/39316948/typeerror-login-takes-1-positional-argument-but-2-were-given
# @login_required ahaha
def login_view(request):     
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                next_page = request.GET['next']
            else:
                next_page = reverse('odp_app:home')
            messages.success(request,"Login effettuato.")
            return redirect(next_page)
        
        else: # if the user has failed auth
            messages.error(request,"Credenziali errate")
    
    # if it's post or it failed
    msgs = list(messages.get_messages(request))

    return render(request, "odp/login.html" )

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,"Logout effettuato con successo")
    return redirect(reverse('odp_app:login'))
