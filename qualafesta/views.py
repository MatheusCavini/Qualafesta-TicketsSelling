from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import *
from django.contrib.auth.models import User

def index(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("qualafesta:login"))
    return render(request, 'index.html', {})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'customer/customer_index.html', {})
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'user_controll/login.html', context)

def logout(request):
    return render(request, 'user_controll/login.html', {})

def register(request):
    return render(request, 'user_controll/register.html', {})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        profile_image = request.POST['profile_image']

        print('\n',first_name, last_name, username,email, password1, password2)
        user_kwargs ={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password1
        }
        user = User.objects.create_user(**user_kwargs)
        if user:
            user.save()
            customer_kwargs = {
                'user_id': user,
                'phone': phone,
                'profile_image':profile_image
            }
            customer = Customer.objects.create(**customer_kwargs)
            print(customer)
            customer.save()
        return HttpResponseRedirect(
            reverse('qualafesta:customer'))
    else:
        form = CustomerRegistrationForm()

    context = {'form': form}
    return render(request, 'user_controll/register_customer.html', context)

def register_organizer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        #if form.is_valid():
        #    form.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        form = CustomerRegistrationForm()

    context = {'form': form}
    return render(request, 'user_controll/register.html', context)


def customer_index(request):
    return render(request, 'customer/customer_index.html', {})