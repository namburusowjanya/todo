from django import forms
from django.contrib.auth.models import User
from .models import Task

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class TaskForm(forms.ModelForm):
    completed=forms.BooleanField(required=False)
    class Meta:
        model=Task
        fields=['title','description','start_date','end_date','completed']