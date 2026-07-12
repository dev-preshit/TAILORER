from django.contrib import admin
from .models import Order, OrderBottomItem, OrderTopItem

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderTopItem)
admin.site.register(OrderBottomItem)
