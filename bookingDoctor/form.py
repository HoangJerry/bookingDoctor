from django.contrib.auth.forms import UserCreationForm
from api.models import *
from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254)
    dob = forms.DateField(required=True )

    class Meta:
        model = UserBase
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address', 'sex', 'role' )

class AppointmentForm(forms.ModelForm):
	class Meta:
		model = Appointment
		fields = ('doctor', 'appointment')
		widgets = {
            'appointment': forms.DateTimeInput(attrs={'id':'datetimepicker4'}),
        }
