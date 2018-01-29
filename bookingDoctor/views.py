# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'home.html')

def logout(request):
    return render(request, 'home.html')