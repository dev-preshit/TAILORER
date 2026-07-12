from django.db import models
from AuthApp.models import Customer
from .constants import GARMENT_TYPES

upperBodyChoice = [
    (name, name) for name, attrs in GARMENT_TYPES.items() if attrs['region'] == 'upper'
]
lowerBodyChoice = [
    (name, name) for name, attrs in GARMENT_TYPES.items() if attrs['region'] == 'lower'
]
allClothsChoice = lowerBodyChoice + upperBodyChoice

buttonChoice = [
    ("Normal","Normal"),
    ("Snap","Snap"),
    ("Flat Shank","Flat Shank"),
    ("Hook","Hook"),
]

sleeveChoice = [
    ("Full","Full"),
    ("Half","Half"),
    ("No Sleeve","No Sleeve"),
]

trouserChoice = [
    ("Normal","Normal"),
    ("Pencil","Pencil"),
    ("",""),
]

materialType = [
    ("cotton","cotton"),
    ("silk","silk"),
    ("wool","wool"),
]


# Create your models here.
class Options(models.Model):
    text = models.TextField(max_length=200)
    upper_body = models.ForeignKey('UpperBody', on_delete=models.CASCADE, null=True, blank=True, related_name='requirements')
    lower_body = models.ForeignKey('LowerBody', on_delete=models.CASCADE, null=True, blank=True, related_name='requirements')

    def __str__(self):
        return self.text
    

class LowerBody(models.Model):
    length = models.IntegerField(default=0)
    waist = models.IntegerField(default=0)
    hips = models.IntegerField(default=0)
    thigh = models.IntegerField(default=0)
    knee = models.IntegerField(default=0)
    ankle = models.IntegerField(default=0)
    pantBottom = models.IntegerField(default=0)
    uCrouch = models.IntegerField(default=0)
    clothType = models.CharField(max_length=20, choices=lowerBodyChoice, default=" ")

    def __str__(self):
        return self.clothType

class UpperBody(models.Model):
    length = models.IntegerField(default=0)
    chest = models.IntegerField(default=0)
    upperChest = models.IntegerField(default=0)
    waist = models.IntegerField(default=0)
    hips = models.IntegerField(default=0)
    shoulder = models.IntegerField(default=0)
    sleeves = models.IntegerField(default=0)
    biceps = models.IntegerField(default=0)
    armHold = models.IntegerField(default=0)
    elbow = models.IntegerField(default=0)
    collar = models.IntegerField(default=0)
    backLength = models.IntegerField(default=0)
    crossBack = models.IntegerField(default=0)
    bustLength = models.IntegerField(default=0)
    apexGap = models.IntegerField(default=0)
    bottomWidth = models.IntegerField(default=0)
    clothType = models.CharField(max_length=20, choices=upperBodyChoice, default=" ")
    pocket = models.BooleanField(default = False)
    button = models.CharField(max_length=20, choices=buttonChoice, default="Normal")
    sleeveType = models.CharField(max_length=20, choices=sleeveChoice, default="Full")

    def __str__(self):
        return self.clothType
    
class ClothPrice(models.Model):
    cloth_type = models.CharField(max_length=20, choices=allClothsChoice, default=" ", unique=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.cloth_type} - ₹{self.base_price}"
    
class Inventory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    typeOfCloth = models.CharField(max_length=30, choices=allClothsChoice, default=" ")
    material = models.CharField(max_length=30, choices=materialType, default=" ")
    image = models.ImageField(upload_to=f'uploads/{customer.name}')
    
    def __str__(self):
        return self.customer.name