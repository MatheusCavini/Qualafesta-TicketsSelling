from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders for the username and password fields
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'



class CustomerRegistrationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    phone = forms.CharField(max_length=255, required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'phone', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Telefone'
        self.fields['profile_image'].widget.attrs['placeholder'] = 'Imagem de perfil'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
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

    def __init__(self, *args, **kwargs):
        super(OrganizerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Telefone'
        self.fields['profile_image'].widget.attrs['placeholder'] = 'Imagem de perfil'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['cnpj'].widget.attrs['placeholder'] = 'CNPJ'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
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
    
    def __init__(self, *args, **kwargs):
        super(AcessControllerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Telefone'
        self.fields['profile_image'].widget.attrs['placeholder'] = 'Imagem de perfil'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirme sua senha'
        self.fields['organization'].widget.attrs['placeholder'] = 'Empresa'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'location',
            'date_time',
            'description',
            'capacity',
            'splash_images',
            'thumb_image',
            'gender',
        ]
        labels = {
            'name' : 'Nome do Evento',
            'location' : 'Localização',
            'date_time' : 'Data',
            'description' : 'Descrição',
            'capacity' : 'Capacidade Máxima', 
            'splash_images' : 'Imagens do Evento',
            'thumb_image' : 'Imagem de Capa',
            'gender' : 'Gênero',
        }

class AttractionForm(ModelForm):
    class Meta:
        model = ArtistParticipation
        fields = [
            'artist_name',
            'begin_time',
            'end_time',
            'artist_image',
        ]
        labels = {
            'artist_name' : 'Nome do Artista',
            'begin_time' : 'Hora de Início',
            'end_time' : 'Hora de Término',
            'artist_image' : 'Imagem do Artista',
        }

