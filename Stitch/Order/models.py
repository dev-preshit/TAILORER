from django.db import models
from AuthApp.models import Customer
from Cloth.models import *
# Create your models here.


orderstatus = [
    ("Confirmed", "Confirmed"),
    ("Processing", "Processing"),
    ("Complated", "Complated"),
    ("Delivered", "Delivered"),
    ("Cenceled", "Cenceled"),
]

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=orderstatus, default="Confirmed")
    in_time = models.DateTimeField(auto_now_add=True)
    days = models.PositiveIntegerField(default=7, help_text="Days to complete the order")
    out_time = models.DateTimeField(null=True, blank=True)
    urgent = models.BooleanField(default=False)

    def __str__(self):
        return self.customer.name

class OrderTopItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tops')
    upper_body = models.ForeignKey(UpperBody, on_delete=models.CASCADE)

class OrderBottomItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='bottoms')
    lower_body = models.ForeignKey(LowerBody, on_delete=models.CASCADE)
