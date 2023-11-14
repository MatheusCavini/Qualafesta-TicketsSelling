from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    phone = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'profile_image']
    
        
class OrganizerRegistrationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    phone = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    cnpj = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'profile_image', 'cnpj']
    
        
class AcessControllerRegistrationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    phone = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    organization = forms.CharField(max_length=255, required  = True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'profile_image', 'organization']
    
        

