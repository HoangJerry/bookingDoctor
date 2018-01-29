# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
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
    adress = models.CharField(max_length=250, null=True, blank=True)
    sex = models.PositiveSmallIntegerField(_('sex'), choices=CONST_GENDERS, \
                                              default=CONST_GENDER_MALE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

class Appointment(models.Model):
    patient = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='doctor')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField()
    
        

