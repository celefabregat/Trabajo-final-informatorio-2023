from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2", "email"]

class LoginForm(forms.Form):
    username = forms.CharField(label= "Nombre de Usuario")
    password = forms.CharField(label= "Contraseña", widget=forms.PasswordInput)

    def login(self, request):
        username = self.cleaned_data.get("username")
        password =self.cleaned_data.get("password")
        user = authenticate(request,username=username, password=password )
        if user:
            login(request, user)

