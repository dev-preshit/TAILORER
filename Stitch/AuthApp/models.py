from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

genderChoice = [
    ("Male", "Male"),
    ("Female", "Female")
]

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = PhoneNumberField()
    gender = models.CharField(max_length=20, choices=genderChoice ,default="Male")
    create_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    