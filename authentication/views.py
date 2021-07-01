from django.shortcuts import render

# Create your views here.
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm

from validate_email import validate_email
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from django.views import View
from django.contrib import messages
from .utils import token_generator


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid credentials")
        else:
            messages.error(request, 'Error validating the form')

    return render(request, "authentication/login.html", {"form": form})


def register_user(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            # user = authenticate(username=username, password=password)

            # user = User.objects.create_user(username=username, email=email)
            user = form.save(commit=False)
            user.set_password(password)
            user.is_active = False
            user.save()

            """
            to send a activate link to the user email
            needs: path to view
                1. getting domain we are on
                2. relative url to verification
                3. encode uid
                4. token
            """
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64,
                                               'token': token_generator.make_token(user)})
            activate_url = 'http://' + domain + link

            email_subject = 'Activate your account'
            email_body = 'Hi ' + user.username + \
                ' Please use this link to verify your account\n ' + activate_url

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@example.com',
                [email],
            )
            EmailThread(email).start()
            messages.success(
                request, 'Account successfully created, please check your email to activate your account')
            return render(request, 'authentication/register.html', {"form": form})

        else:
            messages.error(request, 'form is invalid')
    else:
        form = SignUpForm()

    return render(request, "authentication/register.html", {"form": form})


class RequestPasswordResetEmailView(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']

        context = {'values': request.POST}

        if not validate_email(email):
            messages.error(request, 'Invalid email')

            return render(request, 'authentication/reset-password.html', context)

        user = User.objects.filter(email=email)
        domain = get_current_site(request).domain

        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            link = reverse('reset-password', kwargs={'uidb64': uidb64,
                                                     'token': PasswordResetTokenGenerator().make_token(user[0])})
            reset_url = 'http://' + domain + link

            email_subject = 'Rest your password'
            email_body = 'Hi, Please use this link to reset your password\n ' + reset_url

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@example.com',
                [email],
            )
            # email.send(fail_silently=False)
            EmailThread(email).start()

        messages.success(
            request, 'We have sent you an email to reset password')

        return render(request, 'authentication/reset-password.html')


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')


class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password link is invalid, please request a new one!')

                return render(request, 'authentication/reset-password.html')
        except Exception as e:
            pass

        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, 'Password too short')
            return render(request, 'authentication/set-new-password.html', context)
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password changed successfully!')

            return redirect('login')
        except Exception as e:
            messages.info(request, "Something went wrong, please try again")
            return render(request, 'authentication/set-new-password.html', context)
