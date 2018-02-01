# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from form import *
from api.models import *
from django.contrib.auth import authenticate, login

from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class ProfileUser(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = UserBase
    form_class = UpdateForm
    template_name = 'profile.html'

    def get_success_url(self):
        return u'/profile/%d' % self.request.user.id 


class PatientListView(ListView):
    model = Patient
    template_name = 'patients.html'
    
    def get_queryset(self):
        doctor_id = UserBase.objects.filter( id = self.request.user.id )
        appointment_id = Appointment.objects.filter(doctor_id = 15)
        patient = Patient.objects.filter( patient_appointment = appointment_id)
        return patient


class AppointmentBook(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = "appointment_book.html"
    model = Appointment
    fields = ('doctor', 'appointment')

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        return super(AppointmentBook,self).form_valid(form)


class AppointmentDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
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

class AppointmentMe(LoginRequiredMixin, ListView):
    login_url = '/login/'
    queryset = Appointment.objects.all()
    template_name = 'appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        if self.request.user.role == UserBase.PATIENT:
            return Appointment.objects.filter(patient=self.request.user.patient).order_by('-creation_date')
        return Appointment.objects.filter(doctor=self.request.user.doctor).order_by('appointment')

class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Appointment
    fields = ('doctor', 'appointment')
    template_name = "appointment_book.html"

    def get_object(self, queryset=None):
        return Appointment.objects.filter(patient=self.request.user.patient).order_by('creation_date').last()
