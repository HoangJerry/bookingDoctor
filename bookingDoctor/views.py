# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from form import *
from django.contrib.auth import authenticate, login

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':

        signup_form = SignUpForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()
            patient = Patient.objects.create(user=signup_form.instance, dob=signup_form.cleaned_data.get('dob'))
            username = signup_form.cleaned_data.get('username')
            password1 = signup_form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password1)
            
            if user is not None:
				login(request, user)
				return redirect('home')
        return render(request, 'signup.html', {'signup_form': signup_form})

    else:
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'signup_form': signup_form})
