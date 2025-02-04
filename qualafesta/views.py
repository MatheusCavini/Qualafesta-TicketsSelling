from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_default
from django.views import generic, View
from django.test import RequestFactory
from .models import Event, TicketsOrder, TicketCattegory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import uuid
import cv2
import base64
import json
import qrcode
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random
import string
from django.contrib.auth.mixins import LoginRequiredMixin


######################################################################## Login Views
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("qualafesta:login"))
    user = request.user
    try:
        customer = Customer.objects.get(user_id=user)
        return HttpResponseRedirect(
            reverse('qualafesta:customer'))
    except: pass
    try:
        organizer = Organizer.objects.get(user_id=user)
        return HttpResponseRedirect(
            reverse('qualafesta:organizer_events'))
    except: pass
    try:
        acess_controller = AcessController.objects.get(user_id=user)
        return HttpResponseRedirect(
            reverse('qualafesta:acess_controller'))
    except: pass
    if request.user.is_superuser:
        return redirect('/admin/')
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
                reverse('qualafesta:organizer_events'))
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
                reverse('qualafesta:organizer_events'))
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

def CustomerProfile(request):
    try:
        user_instance = get_object_or_404(Customer, user_id=request.user.id)
    except: 
        try:
            user_instance = get_object_or_404(Organizer, user_id=request.user.id)
        except: 
            user_instance = get_object_or_404(AcessController, user_id=request.user.id)
    
    return render(request, 'customer/customer_profile.html', {'user_instance':user_instance})

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

class EventTicketsView(generic.DetailView):
    model = Event
    template_name = 'customer/customer_eventTickets.html'

@csrf_exempt
@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            # Assuming Customer model has a 'user' field representing the linked User instance
            data = json.loads(request.body)
            price = float(data.get('total_price'))
            order = TicketsOrder.objects.create(
                customer_id=request.user,
                order_date=timezone.now(),
                payment_situation=1,
                total_price=price,
            )
            return JsonResponse({'success': True, 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  # Only for demonstration, consider using a better approach for CSRF protection
def create_purchased_tickets(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Assuming you have the order_id available (modify as needed)
        order_id = data.get('order_id')
        order = get_object_or_404(TicketsOrder, id=order_id)

        # Iterate through the selected tickets and create PurchasedTicket instances
        for ticket_data in data.get('selected_tickets', []):
            ticket_category_id = ticket_data.get('ticket_category_id')
            quantity = ticket_data.get('quantity')

            # Assuming you have a model for TicketCattegory
            ticket_category = get_object_or_404(TicketCattegory, id=ticket_category_id)
            print(ticket_category)

            # Create PurchasedTicket instances
            for _ in range(quantity):
                section1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                section2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                section3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

                # Combine the sections with hyphens
                code = f"{section1}-{section2}-{section3}"
                purchased_ticket = PurchasedTicket.objects.create(
                    ticket_order_id=order,
                    ticket_category_id=ticket_category,
                    hash_code = code,
                )
                ticket_category.sold_amount += 1
                ticket_category.save()
                purchased_ticket.save()
                print(ticket_category.sold_amount)

        return JsonResponse({'success': True, 'message': 'Purchased tickets created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


######################################################################## Organizer Views
def is_organizer(user):
    return user.groups.filter(name='Organizers').exists()

@login_required
@user_passes_test(is_organizer)
def organizer_index(request):
    user_instance = get_object_or_404(Organizer, user_id=request.user.id)
    return render(request, 'organizer/organizer_index.html', {"user_instance":user_instance})

class EventListView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'organizer/organizer_events.html'  
    context_object_name = 'event_list'

    def get_queryset(self):
        return Event.objects.filter(organizer_id=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context
    
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context  
 

class CreateAttractionView(LoginRequiredMixin, generic.CreateView):
    model = ArtistParticipation
    form_class = AttractionForm
    template_name = 'organizer/create_attraction.html'

    def form_valid(self, form):
        # Assume que 'pk' está vindo da URL
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        form.instance.event_id = event
        form.instance.organizer_id = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para a página dos tickets do evento
        return reverse('qualafesta:event_attractions', args=(self.kwargs['pk'],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        context['user_instance'] = user_instance
        context['event'] = event
        return context  
        
    
class CreateEventView(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'organizer/create_event.html'

    def form_valid(self, form):
        form.instance.organizer_id = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return (reverse('qualafesta:organizer_events'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context  


class OrgTicketsView(LoginRequiredMixin, generic.DetailView):
    model = Event
    template_name = 'organizer/organizer_eventTickets.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context

def create_ticket(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        name = request.POST['name']
        description= request.POST['description']
        capacity = request.POST['capacity']
        price = request.POST['price']
        sold_amount = 0
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

class CreateTicketsView(LoginRequiredMixin, generic.CreateView):
    model = TicketCattegory
    form_class = TicketForm
    template_name = 'organizer/create_ticket.html'

    def form_valid(self, form):
        # Assume que 'pk' está vindo da URL
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        form.instance.event_id = event
        form.instance.organizer_id = self.request.user
        form.instance.sold_amount = 0
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para a página dos tickets do evento
        return reverse('qualafesta:event_tickets', args=(self.kwargs['pk'],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(Organizer, user_id=self.request.user.id)
        event = get_object_or_404(Event, id=self.kwargs['pk'])
        context['user_instance'] = user_instance
        context['event'] = event
        return context
    
def organizer_profile(request):
    user_instance = get_object_or_404(Organizer, user_id=request.user.id)
    return render(request, 'organizer/organizer_profile.html', {'user_instance':user_instance})



######################################################################## Acesss Controller Views
def is_acess_controller(user):
    return user.groups.filter(name='AcessControllers').exists()

@login_required
@user_passes_test(is_acess_controller)
@csrf_exempt


def search_event_controller(request):
    user_instance = get_object_or_404(AcessController, user_id=request.user.id)
    context = {'user_instance':user_instance}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        event_list = Event.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))
        if len(event_list) == 0:
            event_list = "nenhum resultado"
        context = {'user_instance':user_instance, "event_list": event_list}
    return render(request, 'acess_controller/search_event_controller.html', context)
      
class EventControllerViews(generic.ListView):
    model = Event
    template_name = 'acess_controller/acess_controller_index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(AcessController, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context

class EventControllView(generic.DetailView):
    model = Event
    template_name = 'acess_controller/controll_event.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_instance = get_object_or_404(AcessController, user_id=self.request.user.id)
        context['user_instance'] = user_instance
        return context


def get_ticket_data(ticket_hash, event_id):
    try:
        purchased_ticket = PurchasedTicket.objects.get(hash_code=ticket_hash)
        ticket_order = purchased_ticket.ticket_order_id
        ticket_cattegory = purchased_ticket.ticket_category_id
        event = ticket_cattegory.event_id 
        user = ticket_order.customer_id 
        customer = Customer.objects.get(user_id=user.id)
        context ={
            'ticket_hash': ticket_hash,
            'event_id': event_id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'profile_image': customer.profile_image,
            'user':user,
            'correct':True,
            'category':ticket_cattegory.name
        }
        if purchased_ticket.status:
            context['correct'] = False
            context['error_message'] ='Este ingresso já foi validado'
        elif ticket_order.payment_situation != 1:
            context['correct'] = False
            context['error_message'] ='O pagamento deste ingresso não foi efetuado'
    except:
        context ={
            'ticket_hash': ticket_hash,
            'event_id': event_id,
            'correct':False,
            'error_message':'Ingresso não encontrado'
        }
    return context

@login_required
@user_passes_test(is_acess_controller)
@csrf_exempt
def ticket_detail(request, pk):
    ticket_hash = request.GET['query']
    context = get_ticket_data(ticket_hash, pk)
    user_instance = get_object_or_404(AcessController, user_id=request.user.id)
    context['user_instance'] = user_instance
    return render(request, 'acess_controller/ticket_data.html', context)

@login_required
@user_passes_test(is_acess_controller)
@csrf_exempt
def validate_ticket(request, event_id, ticket_hash):
    purchased_ticket = PurchasedTicket.objects.get(hash_code=ticket_hash)
    controller_user = request.user
    purchased_ticket.acess_controller_id = controller_user
    purchased_ticket.status = True
    purchased_ticket.entrance = datetime.now()
    purchased_ticket.save()
    return redirect(f'/acess_controller/controll_event{str(event_id)}')

@login_required
@user_passes_test(is_acess_controller)
@csrf_exempt
def scan_qr(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        event_id = received_data.get('event_id')
        image_data = received_data.get('image')
        image_data = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detector = cv2.QRCodeDetector()
        data_str, bbox, _ = detector.detectAndDecode(gray_img)
        if data_str!='':
            redirect_url = f'ticket_detail?query={data_str}'
            return JsonResponse({'message': 'QR code decodificado com sucesso', 
                                 'redirect_url': redirect_url,
                                 'hash_code': data_str})
        else:
            return JsonResponse({'message': 'Nenhum QR code encontrado', 
                                 'redirect_url':None,'hash_code':None})
    else:
        return JsonResponse({'error': 'Invalid request method'})
            
        

def acess_controller_profile(request):
    user_instance = get_object_or_404(AcessController, user_id=request.user.id)
    return render(request, 'acess_controller/acess_controller_profile.html', {'user_instance':user_instance})

def list_events(request):
    event_list = Event.objects.all()
    context = {'event_list': event_list}
    return render(request, 'eventes/index.html', context)
#####################################
def search_events(request):
    user_instance = get_object_or_404(Customer, user_id=request.user.id)
    context = {'user_instance':user_instance}
    if request.GET.get('query', False):
        search_term = request.GET['query'].lower()
        user_instance = get_object_or_404(Customer, user_id=request.user.id)
        event_list = Event.objects.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))
        if len(event_list) == 0:
            event_list = "nenhum resultado"
        context = {'user_instance':user_instance, "event_list": event_list}
    return render(request, 'customer/search.html',context)

def CustomerIndex(request):
    event_list = Event.objects.all()
    user_instance = get_object_or_404(Customer, user_id=request.user.id)
    return render(request, 'customer/customer_index.html', {'user_instance':user_instance, "event_list": event_list})
