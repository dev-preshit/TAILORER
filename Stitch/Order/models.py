from django.db import models
from AuthApp.models import Customer
from Cloth.models import *
# Create your models here.


orderstatus = [
    ("Confirmed", "Confirmed"),
    ("Processing", "Processing"),
    ("Urgent", "Urgent"),
    ("Complated", "Complated"),
    ("Delivered", "Delivered"),
    ("Cenceled", "Cenceled"),
]

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    upperBody = models.ForeignKey(UpperBody, on_delete=models.CASCADE, null=True, blank=True)
    lowerBody = models.ForeignKey(LowerBody, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=orderstatus, default="New")
    in_time = models.DateTimeField(auto_now_add=True)
    days = models.PositiveIntegerField(default=7, help_text="Days to complete the order")
    out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.customer.name
    
