from django import forms
from django.forms import TextInput
from .models import Account

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'PlaceHolder': 'Password', 'Class': 'w-full p-2 border rounded-md focus:outline-none focus:border-blue-500'}), max_length=16)
	class Meta:
		model 	= Account
		fields 	= ('username', 'password',)
		widgets = {
            'username': forms.TextInput(attrs={'PlaceHolder': 'Username', 'class': 'w-full p-2 border rounded-md focus:outline-none focus:border-blue-500'}),
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'PlaceHolder': 'Password', 'Class': 'form-control mt-3'}), max_length=16)
	class Meta:
		model 	= Account
		fields 	= ('username', 'password',)
		widgets = {
            'username': TextInput(attrs={'PlaceHolder': 'Username', 'Class': 'form-control mt-3'}),
        }