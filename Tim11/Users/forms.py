from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone']


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'phone']


