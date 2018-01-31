# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from form import *
from api.models import *
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, FormView
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

class AppointmentBook(FormView):
    template_name = "appointment_book.html"
    form_class = AppointmentForm

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        return super(AppointmentBook,self).form_valid(form)


class AppointmentDetail(DetailView):
    queryset = Appointment.objects.all()
    template_name = 'appointment_detail.html'
    context_object_name = 'appointment'
    def get_object(self):
        # Call the superclass
        object = super(AppointmentDetail,self).get_object()
        # Record the last accessed date
        object.last_change = timezone.now()
        object.save()
        # Return the object
        return object
