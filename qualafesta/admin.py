from django.contrib import admin

from .models import * 

admin.site.register(Event)
admin.site.register(ArtistParticipation)
admin.site.register(TicketCattegory)
admin.site.register(TicketsOrder)
admin.site.register(PurchasedTicket)
admin.site.register(Customer)
admin.site.register(Organizer)
admin.site.register(AcessController)