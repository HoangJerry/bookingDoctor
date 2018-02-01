# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class UserBase(AbstractUser):
    PATIENT = 1
    DOCTOR = 2
    ROLE_CHOICES = (
        (PATIENT, _('Patient')),
        (DOCTOR, _('Doctor')),
    )

    CONST_GENDER_FEMALE = 0
    CONST_GENDER_MALE = 1
    CONST_GENDER_BOTH = 2
    CONST_GENDERS = (
        (CONST_GENDER_FEMALE, _('Female')),
        (CONST_GENDER_MALE, _('Male')),
        (CONST_GENDER_BOTH, _('Both')),
    )

    phone = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    sex = models.PositiveSmallIntegerField(_('sex'), choices=CONST_GENDERS, \
                                              default=CONST_GENDER_MALE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=DOCTOR, null=True, blank=True)

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name,self.last_name)

class Patient(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    dob = models.DateField(_('DOB'), null=True, blank=True)

    def __unicode__(self):
        return self.user.full_name

# @receiver(post_save, sender=UserBase)
# def create_patient(sender, instance, created, **kwargs):
#     if created and instance.role==UserBase.PATIENT:
#         Patient.objects.create(user=instance)

class Doctor(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE)
    category = models.CharField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.user.full_name

@receiver(post_save, sender=UserBase)
def create_doctor(sender, instance, created, **kwargs):
    if created and instance.role==UserBase.DOCTOR:
        Doctor.objects.create(user=instance)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_appointment')
    doctor = models.ForeignKey(Doctor, related_name='doctor_appointment')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    appointment = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = timezone.now()
        super(Appointment, self).save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse('appointment-detail', kwargs={'pk': self.pk})
        
class Treatment(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_treatment')
    doctor = models.ForeignKey(Doctor, related_name='doctor_treatment')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    treatment = models.CharField(max_length=250, null=True, blank=True)
    treatment_for = models.CharField(max_length=250, null=True, blank=True)
    dnote = models.CharField(max_length=250, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = timezone.now()
        super(Treatment, self).save(force_insert, force_update, using, update_fields)

class Schedule(models.Model):    
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = timezone.now()
        super(Schedule, self).save(force_insert, force_update, using, update_fields)

class Feedback(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_feedback')
    creation_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()