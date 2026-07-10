from django.urls import path
from Order import views


urlpatterns = [
    path("", views.home, name="home"),
    path("order/", views.getAllOrders, name="allOrders"),
    path("order/add/", views.addOrder, name = "addOrder"),
    path("order/gender/", views.orderGender, name="orderGender"),
    path("order/<int:pk>/", views.getOrder, name = "order"),
    path("order/add/<str:cloth>", views.addCloth, name = "addCloth"),
    path("garmentPicker/",views.garmentPicker, name="garmentPicker"),
    path("order/cancel/", views.cancelOrder, name="cancelOrder"),
    path("order/live-search/", views.liveSearch, name="liveSearch"),

]