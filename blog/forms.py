from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import post


class user_signup_form(UserCreationForm):
    password1 = forms.CharField(
        label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again):',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter valid email address'})
        }


class user_login_form(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class EditUserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class add_post_form(forms.ModelForm):
    class Meta:
        model = post
        fields = ['title', 'desc']
        # fields = ['user', 'title', 'desc']
        labels = {'desc': 'Description'}
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   #    'user': forms.ChoiceField(attrs={'class': 'form-control'}),
                   }
