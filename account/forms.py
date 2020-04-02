from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


from .models import Profile

class CreateUserForm(UserCreationForm):
    email =forms.CharField(required=False,
                           widget=forms.TextInput
                           (attrs={"class": "form-control my-2",
                                   'id': 'Email',
                                   'placeholder': 'EMAIL'})
                           )

    class Meta:
        model = User
        fields=['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control my-2",
              'id': 'Username',
              'placeholder':'USERNAME *',}),

            'email': forms.TextInput(
                                     attrs={"class": "form-control my-2",
               'id': 'Email',
               'placeholder': 'Email',
               'required':'false'}),

            'password1': forms.TextInput(attrs={"class": "form-control my-2",
               'id': 'Password',
               'placeholder': 'PASSWORD*', }),

            'password2': forms.TextInput({"class": "form-control my-2",
               'id': 'cPassword',
               'placeholder': 'CONFIRM PASSWORD*', }),
        }



class CreateProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['phone_number'].required = False

    first_name = forms.CharField(max_length=20,

                                 widget=forms.TextInput
                                 (attrs={"class": "form-control my-2",
                                         'id': 'FName',
                                         'placeholder':'FIRST NAME *'}))
    middle_name = forms.CharField(max_length=20,
                                required = False,
                                  widget=forms.TextInput
                                  (attrs={"class": "form-control my-2",
                                          'id': 'MName',
                                          'placeholder':'MIDDLE NAME ',
                                          }))
    last_name = forms.CharField(max_length=20,

                                widget=forms.TextInput
                                (attrs={"class": "form-control my-2",
                                        'id': 'LName',
                                        'placeholder':'LAST NAME *',
                                        }))



    class Meta:
        model = Profile
        fields=['first_name','middle_name','last_name','gender','country','phone_number']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control my-2', 'id': 'Country'}),
            'gender': forms.Select(attrs={'class': 'form-control my-2', 'id': 'Gender'}),
        }
        required=('first_name','last_name')

class ProfileUpdateForm(ModelForm):


    class Meta:
        model = Profile
        fields=['first_name','middle_name','last_name','gender']

