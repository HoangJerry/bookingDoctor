# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AdminPasswordChangeForm
from models import *

class DoctorInline(admin.StackedInline):
    model = Doctor
    can_delete = False
    verbose_name_plural = 'Doctor information'

class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    verbose_name_plural = 'Patient information'

class UserBaseAdmin(UserAdmin):
    list_filter = ('role',)
    list_display = ('id','name','phone',
            'address','sex','role')
    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name','phone',
            'address','sex','role')}),
    )
    
    inlines = (DoctorInline, PatientInline)

    def name(self,obj):
        return obj.full_name

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if isinstance(inline, DoctorInline) and obj is None:
                continue
            if isinstance(inline, PatientInline) and obj is None:
                continue
            if obj:
                if obj.role == UserBase.DOCTOR and isinstance(inline, PatientInline):
                    continue
                if obj.role == UserBase.PATIENT and isinstance(inline, DoctorInline):
                    continue
            yield inline.get_formset(request, obj), inline

# class UserBaseField(admin.ModelAdmin):
#     list_display = ('address','phone','sex',)

#     def address(self,obj):
#         return obj.user.address

#     def phone(self,obj):
#         return obj.user.phone

#     def sex(self,obj):
#         return obj.user.get_sex_display()

# class PatientAdmin(UserBaseField):
#     list_display = ('dob',) + UserBaseField.list_display 


# class DoctorAdmin(UserBaseField):
#     list_display = ('name','category',) + UserBaseField.list_display 

#     def name(self,obj):
#         return u'{} {}'.format(obj.user.first_name,obj.user.last_name)
class AppointmentForm(forms.ModelForm):
    class Meta:
        exclude = ('last_change',)

class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('patient','doctor','appointment','creation_date','last_change')
    list_filter = ('appointment',)

    def has_add_permission(self, request):
        return False

class TreatmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('patient','doctor','creation_date','last_change') 

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('patient','feedback','creation_date',) 
    list_filter = ('creation_date',)

    def has_add_permission(self, request):
        return False

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('creation_date','note','last_change',) 
    list_filter = ('creation_date',)
    # date_hierarchy = 'creation_date'

# admin.site.register(Patient,PatientAdmin)
# admin.site.register(Doctor,DoctorAdmin)

admin.site.register(Schedule,ScheduleAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Treatment,TreatmentAdmin)
admin.site.register(UserBase,UserBaseAdmin)