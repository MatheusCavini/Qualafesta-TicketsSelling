from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_default
import uuid
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from qualafesta.decorators import group_required
from django.views import generic, View
from .models import Event
from django.shortcuts import get_object_or_404
import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


######################################################################## Login Views
def index(request):
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
            return HttpResponseRedirect(
                reverse('qualafesta:customer'))
        except: pass
        try:
            organizer = Organizer.objects.get(user_id=user)
            return HttpResponseRedirect(
                reverse('qualafesta:organizer'))
        except: pass
        try:
            acess_controller = AcessController.objects.get(user_id=user)
            return HttpResponseRedirect(
                reverse('qualafesta:acess_controller'))
        except: pass
        if request.user.is_superuser:
            return redirect('/admin/')
    
    form = CustomAuthenticationForm()
    context = {'form': form}
    return render(request, 'user_controll/login.html', context)

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
        profile_image = None
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
    if request.method == 'POST':
        user = user_register(request)
        phone = request.POST['phone']
        profile_image = None
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

def register_acess_controller(request):
    if request.method == 'POST':
        user = user_register(request)
        phone = request.POST['phone']
        profile_image = None
        organization = request.POST['organization']
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
            group = Group.objects.get(name='AcessControllers')
            group.user_set.add(user)
            acess_controller_kwargs = {
                'user_id': user,
                'phone': phone,
                'profile_image':profile_image,
                'organization':organization
            }
            acess_controller = AcessController.objects.create(**acess_controller_kwargs)
            acess_controller.save()
            return HttpResponseRedirect(
                reverse('qualafesta:acess_controller'))
    else:
        form = AcessControllerRegistrationForm()
    context = {'form': form, 'type_user':'acess_controller'}
    return render(request, 'user_controll/register.html', context)


######################################################################## Customer Views
def is_customer(user):
    return user.groups.filter(name='Customers').exists()

@login_required
@user_passes_test(is_customer)
def customer_index(request):
    return render(request, 'customer/customer_index.html', {})

class EventAboutView(generic.DetailView):
    model = Event
    template_name = 'customer/customer_eventAbout.html'

class EventAttractionsView(generic.DetailView):
    model = Event
    template_name = 'customer/customer_eventAttractions.html'

def TicketsListViews(request):
    ticketsorder = TicketsOrder.objects.filter(customer_id=request.user.id)
    user_instance = get_object_or_404(Customer, user_id=request.user.id)
    return render(request, 'customer/customer_ticketsList.html', {'ticketsorder': ticketsorder, 'user_instance':user_instance})

def generate_qr_code(request, text):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Response with the image content
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


######################################################################## Organizer Views
def is_organizer(user):
    return user.groups.filter(name='Organizers').exists()

@login_required
@user_passes_test(is_organizer)
def organizer_index(request):
    user_instance = get_object_or_404(Organizer, user_id=request.user.id)
    return render(request, 'organizer/organizer_index.html', {"user_instance":user_instance})

#def organizer_events(request):
#   user_instance = get_object_or_404(Organizer, user_id=request.user.id)
#   return render(request, 'organizer/organizer_events.html', {"user_instance":user_instance})
class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer/create_event.html'
    #fields = ['name', 'location', 'date_time', 'description', 'capacity', 'splash_images', 'thumb_image', 'gender']
    # Adicione todos os campos necessários do seu modelo Event

    def form_valid(self, form):
        # Define o organizador do evento como o usuário logado
        form.instance.organizer_id = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return (reverse('qualafesta:organizer_events'))  
    
class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'organizer/organizer_events.html'  
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.filter(organizer_id=self.request.user)
    
class OrgEventAboutView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizer/detail_event.html'

class OrgAttractionsView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizer/organizer_eventAttractions.html'

class UpdateEventView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer/update_event.html'

    def form_valid(self, form):
        form.instance.organizer_id = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return (reverse('qualafesta:organizer_events'))  

def create_attraction(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = AttractionForm(request.POST)
        artist_name = request.POST['artist_name']
        begin_time = request.POST['begin_time']
        end_time = request.POST['end_time']
        artist_image = None
        try:
            artist_image = request.FILES['artist_image']
            if artist_image:
                original_name = artist_image.name
                unique_name = f"{uuid.uuid4().hex}_{original_name}"
                artist_image.name = unique_name
        except:
            pass
        artist_kwargs = {
                'event_id': event,
                'artist_name':artist_name,
                'begin_time':begin_time,
                'end_time':end_time,
                'artist_image':artist_image
            }
        artist = ArtistParticipation.objects.create(**artist_kwargs)
        artist.save()
        return HttpResponseRedirect(
                reverse('qualafesta:event_attractions', args=(event.id, )))
    else:
        form = AttractionForm()
        context = {'form': form, 'event': event}
        return render(request, 'organizer/create_attraction.html', context)    
    
class OrgTicketsView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizer/organizer_eventTickets.html'

def create_ticket(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        name = request.POST['name']
        description= request.POST['description']
        capacity = request.POST['capacity']
        price = request.POST['price']
        sold_amount = request.POST['sold_amount']
        ticket_kwargs = {
                'event_id': event,
                'name':name,
                'description':description,
                'capacity':capacity,
                'price':price,
                'sold_amount':sold_amount
            }
        ticket = TicketCattegory.objects.create(**ticket_kwargs)
        ticket.save()
        return HttpResponseRedirect(
                reverse('qualafesta:event_tickets', args=(event.id, )))
    else:
        form = TicketForm()
        context = {'form': form, 'event': event}
        return render(request, 'organizer/create_ticket.html', context)   


######################################################################## Acesss Controller Views
def is_acess_controller(user):
    return user.groups.filter(name='AcessControllers').exists()

@login_required
@user_passes_test(is_acess_controller)
def acess_controller_index(request):
    return render(request, 'acess_controller/acess_controller_index.html', {})
