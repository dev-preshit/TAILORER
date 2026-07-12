from django.db import models

from Order.models import Order

# Create your models here.

paymentStatusChoice = [
    ("Balance","Balance"),
    ("Paid","Paid"),
]

class recipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    issued_at = models.DateField(auto_now_add=True)
    totalAmount = models.DecimalField(max_digits=5,decimal_places= 2,null=False, blank=False)
    paidAmout = models.DecimalField(max_digits=5,decimal_places= 2,null=False, blank=False)
    paymentStatus = models.CharField(max_length=20, choices=paymentStatusChoice, default="Balance") 

class product(models.Model):
    recipt_id = models.ForeignKey(recipt, on_delete=models.CASCADE)
    cloth = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=5,decimal_places= 2,null=False, blank=False)