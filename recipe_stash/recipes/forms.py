from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CreationForm(UserCreationForm):
    email = forms.EmailField()
    bio = forms.TextInput()
    public = forms.BooleanField(initial=True, required=False)
    class Meta:
        model = Profile
        fields = ('username', 'email', 'first_name',
                  'last_name', 'password1', 'password2',
                  'bio', 'public')
