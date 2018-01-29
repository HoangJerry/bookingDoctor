# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from models import *

class UserBaseAdmin(UserAdmin):
	list_filter = ('role',)
	fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name','phone',
         	'address','sex','role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
class UserBaseField(admin.ModelAdmin):
	list_display = ('address','phone','sex','category',)

	def address(self,obj):
		return obj.user.address

	def phone(self,obj):
		return obj.user.phone

	def sex(self,obj):
		return obj.user.get_sex_display()

class PatientAdmin(UserBaseField):
	list_display = ('dob',)

class DoctorAdmin(UserBaseField):
	list_display = ('name',) + UserBaseField.list_display 

	def name(self,obj):
		return u'{} {}'.format(obj.user.first_name,obj.user.last_name)

	

admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(UserBase,UserBaseAdmin)