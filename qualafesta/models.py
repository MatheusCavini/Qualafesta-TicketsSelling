from django.db import models
from django.conf import settings


class TicketsOrder(models.Model):
    customer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    payment_situation = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.customer_id} {self.order_date} {self.payment_situation} {self.total_price}"
  