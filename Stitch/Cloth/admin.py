from django.contrib import admin
from .models import LowerBody,UpperBody,Options,ClothPrice, Inventory

# Register your models here.
admin.site.register(LowerBody)
admin.site.register(UpperBody)
admin.site.register(Options)
admin.site.register(ClothPrice)
admin.site.register(Inventory)

