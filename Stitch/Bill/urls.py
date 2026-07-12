from django.urls import path
from Bill import views


urlpatterns = [
    path("", views.checkout, name="checkout"),

]