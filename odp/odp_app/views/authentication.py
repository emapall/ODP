import logging

from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from odp_app.forms import SignupForm, PasswordResetForm, SetPasswordForm
from odp_app.models import User
from odp_app.tasks import send_simple_email

token_generator = PasswordResetTokenGenerator()

logger = logging.getLogger(__name__)


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


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # get the parameters to build the mail
            uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            msg = render_to_string(
                    "mail/account_activation.html",
                    {
                        "uid_b64":uid_b64,
                        "token":token,
                        "user":user,
                    }
                )
            sub = "Attiva il tuo account ODP"
            to = [user.email]
            send_simple_email(sub,msg,to,schedule=5)
            return render(request,"messages/signup_mail_sent.html")

    else:
        form = SignupForm()

    return render(request,"odp/signup.html",{"form":form})

def signup_confirm(request,uid_b64,token):
    error_flag = False 
    try:
        user_pk = urlsafe_base64_decode(uid_b64)
        user = User.objects.get(pk=user_pk)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        error_flag = True
    if not error_flag: #if it's false
        error_flag = not token_generator.check_token(user,token) # then keep false on good tokens
    
    if error_flag: #TODO: NOTE BEFORE CHANGING THIS TEMPLATE, look into password reset
        return render(request,"errors/signup_failed.html")
    user.is_active = True
    user.save()
    return render(request,"messages/signup_completed.html",{"user":user})

def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            q = User.objects.filter(email=email)
            try:
                user_list = [ q.get() ]
                multi_account = False
            except(User.MultipleObjectsReturned, User.DoesNotExist):
                if q.count() > 1:
                    multi_account = True
                    user_list = q
                else:
                    return render(request,"errors/password_reset_user_not_found.html", {"email":email})
            
            # after having taken the user(s)
            for user in user_list:
                uid_b64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                msg = render_to_string(
                    "mail/password_reset.html",
                    {
                        "uid_b64":uid_b64,
                        "token":token,
                        "user":user,
                        "multi_account":multi_account
                    }
                )
                sub = "Ripristino credenziali ODP"
                send_simple_email(sub,msg,[email],schedule=5)
                
            return render(request,"messages/signup_mail_sent.html")

    else: # if form is not valid
        form = PasswordResetForm()
    
    return render(request,"odp/singup.html",{"form":form})

def password_reset_confirm(request,uid_b64,token):
    # FIRST, CHECK TOKEN AND GET USER
    error_flag = False 
    try:
        user_pk = urlsafe_base64_decode(uid_b64)
        user = User.objects.get(pk=user_pk)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        error_flag = True
    if not error_flag: # if it's false 
        error_flag = not token_generator.check_token(user,token) # then keep false on good tokens
    if error_flag: # the template works well for now
        return render(request,"errors/signup_failed.html")

    # IF TOKEN & USER CORRECT, ELABORATE THE REQUEST
    if request.method == "POST":
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            return render(request,"messages/passowrd_reset_completed.html",{"user":user})
    else:
        form = SetPasswordForm()
    
    return render(request,"odp/singup.html",{"form":form})
