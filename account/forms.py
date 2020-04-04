from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile

class CreateUserForm(UserCreationForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields=['username','email','first_name','last_name', 'password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": "input",}),

            'email': forms.EmailInput(attrs={"class": "input",}),

            'password1': forms.Textarea(attrs={'placeholder':'Password',}),

            'password2': forms.PasswordInput(attrs={'placeholder':'Confirm Password',}),
        }

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ('users','followings', 'followers',)

