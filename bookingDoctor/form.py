from django.contrib.auth.forms import UserCreationForm
from api.models import *
from django import forms

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254,required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField( required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.BooleanField( required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserBase
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address', 'sex', 'role' )

class UpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254,required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(required=True, label = 'Birthday', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField( required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField( choices =((0, 'Female'), (1, 'Male'), (2, 'Both')), label = 'Gender', widget=forms.Select(attrs={'class': 'form-control'}) )
    
    
    class Meta:
        model = UserBase
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'sex' )
        


class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
		fields = ('doctor', 'appointment')
		widgets = {
            'appointment': forms.DateTimeInput(attrs={'id':'datetimepicker4'}),
        }
