from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_default
import uuid
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("qualafesta:login"))
    return render(request, 'index.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_default(request, user)
            context={'user':user}
        try:
            customer = Customer.objects.get(user_id=user)
            context['customer'] = customer
            return render(request, 'customer/customer_index.html', context)
        except: pass
        try:
            organizer = Organizer.objects.get(user_id=user)
            context['organizer'] = organizer
            return render(request, 'organizer/organizer_index.html', context)
        except: pass
    
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'user_controll/login.html', context)

def logout(request):
    return render(request, 'user_controll/login.html', {})

def register(request):
    return render(request, 'user_controll/register.html', {})

def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        user_kwargs ={
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password
        }
        user = User.objects.create_user(**user_kwargs)
        return user

def register_customer(request):
    if request.method == 'POST':
        user = user_register(request)
        phone = request.POST['phone']
        profile_image = request.POST['profile_image']
        try:
            profile_image = request.FILES['profile_image']
            if profile_image:
                original_name = profile_image.name
                unique_name = f"{uuid.uuid4().hex}_{original_name}"
                profile_image.name = unique_name
        except:
            pass
        if user:
            login_default(request,user)
            user.save()
            group = Group.objects.get(name='Customers')
            group.user_set.add(user)
            customer_kwargs = {
                'user_id': user,
                'phone': phone,
                'profile_image':profile_image
            }
            customer = Customer.objects.create(**customer_kwargs)
            customer.save()
            return HttpResponseRedirect(
                reverse('qualafesta:customer'))
    else:
        form = CustomerRegistrationForm()
    context = {'form': form, 'type_user':'customer'}
    return render(request, 'user_controll/register.html', context)

def register_organizer(request):
    print(request)
    if request.method == 'POST':
        user = user_register(request)
        phone = request.POST['phone']
        profile_image = request.POST['profile_image']
        cnpj = request.POST['cnpj']
        try:
            profile_image = request.FILES['profile_image']
            if profile_image:
                original_name = profile_image.name
                unique_name = f"{uuid.uuid4().hex}_{original_name}"
                profile_image.name = unique_name
        except:
            pass
        if user:
            login_default(request,user)
            user.save()
            group = Group.objects.get(name='Organizers')
            group.user_set.add(user)
            organizer_kwargs = {
                'user_id': user,
                'phone': phone,
                'profile_image':profile_image,
                'cnpj':cnpj
            }
            organizer = Organizer.objects.create(**organizer_kwargs)
            organizer.save()
            return HttpResponseRedirect(
                reverse('qualafesta:organizer'))
    else:
        form = OrganizerRegistrationForm()
    context = {'form': form, 'type_user':'organizer'}
    return render(request, 'user_controll/register.html', context)


@login_required
def customer_index(request):
    print(request.user, request.user.is_authenticated)
    return render(request, 'customer/customer_index.html', {})

@login_required
def organizer_index(request):
    print(request.user, request.user.is_authenticated)
    return render(request, 'organizer/organizer_index.html', {})