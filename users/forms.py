from django.forms import ModelForm
from .models import User


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "mobile", "role", "password","assembly")


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
