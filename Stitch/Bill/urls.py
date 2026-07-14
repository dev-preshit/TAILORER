from django.urls import path
from Bill import views


urlpatterns = [
    path("<int:id>", views.checkout, name="checkout"),


]