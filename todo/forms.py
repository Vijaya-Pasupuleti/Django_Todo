from django import forms
from django.contrib.auth.models import User

from . import models


class BoardForm(forms.ModelForm):
    name = forms.CharField(max_length=250, required=True, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Board Name'}))

    class Meta:
        model = models.Board
        fields = ['name']


class TaskForm(forms.ModelForm):
    description = forms.CharField(max_length=256, required=True, label='', widget=forms.TextInput(
        attrs={'placeholder': 'Task Description'}))

    class Meta:
        model = models.Task
        fields = ['description']


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterUserForm(forms.Form):
    username = forms.CharField(max_length=50, label="Username")
    password = forms.CharField(
        max_length=20, label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(
        max_length=20, label="Confirm password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username is available, please change username")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords did not match!")
        values = {
            "username": username,
            "password": password,
            "confirm": confirm,
        }
        return values
