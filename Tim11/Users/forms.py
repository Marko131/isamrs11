from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_messages={"asd": '123'})

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'city', 'phone_number']