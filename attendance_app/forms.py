from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'employee_id', 'email']
        widgets = {
            # 'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'name': forms.TextInput(attrs={
                'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-3',
                'placeholder': 'Enter your name',
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-3',
                'placeholder': 'Enter your employee ID',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-3',
                'placeholder': 'Enter your email',
            }),
        }