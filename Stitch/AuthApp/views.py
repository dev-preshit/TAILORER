from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer
from .forms import CustomerForm, UserRegisterForm

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'AuthApp/login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'form': form 
    }
    return render(request, 'AuthApp/registration.html', context)


def logout_view(request):
    logout(request)
    return redirect("login_view")

def allCustomer(request):
    customers = Customer.objects.all()
    context = {
        'customers' : customers,
    }
    return render(request, 'AuthApp/allCustomer.html', context=context)

def addCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('allCustomer')
    else:
        form = CustomerForm()
    context = {
        'form' : form,
        'form_action': 'addCustomer'
    }
    return render(request, 'AuthApp/addCustomer.html', context)

def editCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(data=request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('allCustomer')
        
    else:
        form = CustomerForm(instance = customer)
    context = {
        'form' : form,
        'form_action': 'editCustomer',
        'pk': pk  
    }
    return render(request, 'AuthApp/editCustomer.html', context)

def deleteCustomer(request, pk):
    customer = get_object_or_404(Customer,pk=pk)
    customer.delete()
    return redirect('allCustomer')