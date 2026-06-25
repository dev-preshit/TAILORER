from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name = 'login_view'),
    path('signup/', views.signup_view, name = 'signup_view'),
    path('logout/', views.logout_view, name = 'logout_view'),
    path('customer/', views.allCustomer, name= 'allCustomer'),
    path('customer/add', views.addCustomer, name= 'addCustomer'),
    path('customer/edit/<int:pk>', views.editCustomer, name= 'editCustomer'),
    path('customer/delete/<int:pk>', views.deleteCustomer, name= 'deleteCustomer'),
]
