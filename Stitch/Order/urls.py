from django.urls import path
from Order import views


urlpatterns = [
    path("", views.getAllOrders, name="allOrders"),
    path("add/", views.addOrder, name = "addOrder"),
    path("gender/", views.orderGender, name="orderGender"),
    path("<int:id>/", views.getOrder, name = "order"),
    path("add/<str:cloth>", views.addCloth, name = "addCloth"),
    path("garmentPicker/",views.garmentPicker, name="garmentPicker"),
    path("cancel/", views.cancelOrder, name="cancelOrder"),
]