from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm
from datetime import datetime

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
    name = forms.CharField(max_length=255, required=True)
    location = forms.CharField(max_length=255, required=True)
    date_time = forms.DateTimeField(required=True, initial=datetime.now())
    description = forms.CharField(max_length=255, required=True)
    capacity = forms.IntegerField(required=True)
    splash_images = forms.ImageField(required=True)
    thumb_image = forms.ImageField(required=True)
    gender = forms.CharField(max_length=255, required=True)

    class Meta:
        model = ArtistParticipation
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
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['location'].widget.attrs['placeholder'] = 'Localização'
        self.fields['date_time'].widget.attrs['placeholder'] = 'Data'
        self.fields['description'].widget.attrs['placeholder'] = 'Descrição'
        self.fields['capacity'].widget.attrs['placeholder'] = 'Capacidade Máxima'
        self.fields['splash_images'].widget.attrs['placeholder'] = 'Imagens do Evento'
        self.fields['thumb_image'].widget.attrs['placeholder'] = 'Imagem de Capa'
        self.fields['gender'].widget.attrs['placeholder'] = 'Gênero'


class AttractionForm(ModelForm):
    artist_name = forms.CharField(max_length=255, required=True)
    begin_time = forms.DateTimeField(required=True, initial=datetime.now())
    end_time = forms.DateTimeField(required=True, initial=datetime.now())
    artist_image = forms.ImageField(required=False)

    artist_name.label = "Nome da atração"
    begin_time.label = "Horário de início"
    end_time.label = "Horário de término"
    artist_image.label = "Imagem"

    class Meta:
        model = ArtistParticipation
        fields = fields = [
            'artist_name',
            'begin_time',
            'end_time',
            'artist_image',
        ]

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['artist_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['begin_time'].widget.attrs['placeholder'] = 'Hora de Início'
        self.fields['end_time'].widget.attrs['placeholder'] = 'Hora de Fim'
        self.fields['artist_image'].widget.attrs['placeholder'] = 'Imagem do artista'

class TicketForm(ModelForm):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=255, required=True)
    capacity = forms.IntegerField(required=True)
    price = forms.IntegerField(required=True)
    sold_amount = forms.IntegerField(required=True)

    class Meta:
        model = ArtistParticipation
        fields = fields = [
            'name',
            'description',
            'capacity',
            'price',
            'sold_amount',
        ]
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['description'].widget.attrs['placeholder'] = 'Descrição'
        self.fields['capacity'].widget.attrs['placeholder'] = 'Capacidade'
        self.fields['price'].widget.attrs['placeholder'] = 'Preço'
        self.fields['sold_amount'].widget.attrs['placeholder'] = 'Quantidade Vendida'