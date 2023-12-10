from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']