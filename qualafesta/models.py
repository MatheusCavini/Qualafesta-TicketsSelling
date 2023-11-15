from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Customer(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    phone = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="images/profile_images/", blank=True, null=True)

    def __str__(self):
        return f"customer: {self.user_id} - {self.phone} "
    
class Organizer(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='images/profile_images/', blank=True, null=True)
    cnpj = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"organizer: {self.user_id}  - {self.phone} - {self.cnpj} "
    
class AcessController(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/profile_images/', blank=True, null=True)
    organization = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f"acess controller"

class Event(models.Model):
    organizer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    description = models.CharField(max_length=255)
    capacity = models.IntegerField()
    splash_images = models.ImageField(upload_to='images/event_images/', blank=True, null=True)
    thumb_image = models.ImageField(upload_to='images/event_images/', blank=True, null=True)
    gender = models.CharField(max_length=255)

    def __str__(self):
        return f"event: {self.name} - {self.date_time} - {self.location} - {self.description}"
    
class ArtistParticipation(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=255)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    artist_image = models.ImageField(upload_to='images/artist_images/', blank=True, null=True)

    def __str__(self):
        return f"artist participatio: {self.artist_name} - {self.begin_time} - {self.end_time}"

class TicketCattegory(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sold_amount = models.IntegerField()

    def __str__(self):
        return f"ticket category: {self.name} - {self.description} - {self.capacity} - {self.price} - {self.sold_amount}"

class TicketsOrder(models.Model):
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    payment_situation = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"ticket order: {self.customer_id} - {self.order_date} - {self.payment_situation} - {self.total_price}"


class PurchasedTicket(models.Model):
    acess_controller_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_order_id = models.ForeignKey(TicketsOrder, on_delete=models.CASCADE)
    ticket_category_id = models.ForeignKey(TicketCattegory, on_delete=models.CASCADE)
    hash_code = models.CharField(max_length=255)
    entrance = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"purchased_ticker: {self.acess_controller_id} - {self.ticket_order_id} - {self.ticket_category_id} - {self.entrance} - {self.status}"
