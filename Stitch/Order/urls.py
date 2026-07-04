from django.urls import path
from django.views.generic import TemplateView
from Order import views


urlpatterns = [
    # path("",TemplateView.as_view(template_name='home.html'), name="home")
    path("order/", views.getAllOrders, name = "home"),
    path("order/add/", views.addOrder, name = "addOrder"),
    path("order/gender/", views.orderGender, name="orderGender"),
    path("order/<int:pk>/", views.getOrder, name = "order"),
    path("order/add/<str:cloth>", views.addCloth, name = "addCloth"),
    path("garmentPicker/",views.garmentPicker, name="garmentPicker"),
    path("order/cancel/", views.cancelOrder, name="cancelOrder"),
]