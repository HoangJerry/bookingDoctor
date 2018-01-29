# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from models import *

class UserAdmin(UserAdmin):
	fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name','phone',
         	'adress','sex','role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserBase,UserAdmin)