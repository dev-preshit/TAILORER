from django.shortcuts import get_object_or_404, redirect, render

from Order.models import Order
from Cloth.forms import LowerBodyForm, LowerOptionsFormSet, UpperBodyForm, UpperOptionsFormSet
from .forms import OrderForm
from Cloth.constants import GARMENT_TYPES


# Create your views here.
def getAllOrders(request):
    orders = Order.objects.all()
    return render(request, 'Order/allOrders.html', context= {'orders' : orders})

def getOrder(request,pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'Order/orders.html', context= {'order' : order})



# ____________add order flow_______________

def orderGender(request):
    if request.method == "POST":
        gender = request.POST.get('gender')
        request.session['gender'] = {
            'gender':gender
        }
        return redirect('addOrder')
    return render(request, "Order/gender.html")
    
def addOrder(request):
    if request.method == 'POST':
        Customer = request.POST.get('customer')
        Upper = request.POST.get('upperBody')
        Lower = request.POST.get('lowerBody')
        indate = request.POST.get('status')
        days = request.POST.get('days')
        outdate = request.POST.get('out_time')

        request.session['draft_order'] = {
            'Customer' : Customer,
            'Upper':Upper,
            'Lower':Lower,
            'indate':indate,
            'days':days,
            'outdate':outdate,
            } 

        return redirect('garmentPicker')
    
    form = OrderForm()
    return render(request,"Order/addOrder.html",{'form' : form})

def garmentPicker(request):
    draft = request.session.get('draft_order')
    gender = request.session.get('gender')
    request.session['draft_gender'] = {
        "gender" : gender['gender'],
        "draft" : draft
            }
    garments = getGarmentByGender(gender['gender'])
    context = {
        'garments' : garments,
        'draft' : draft,
    }
    return render(request, 'Order/garment_picker.html', context=context)

def addCloth(request, cloth):
    region = getRegionByGarment(cloth)
    draft = request.session.get('draft_gender')

    FormSetClass = UpperOptionsFormSet if region == 'upper' else LowerOptionsFormSet

    if request.method == 'POST':
        form = get_garment_form(cloth, region, data=request.POST)
        formset = FormSetClass(request.POST)

        if form.is_valid() and formset.is_valid():
            garment = form.save()             
            formset.instance = garment         
            formset.save()                      
            return redirect('garmentPicker')
    else:
        form = get_garment_form(cloth, region)
        formset = FormSetClass()

    context = {
        'cloth': cloth,
        'form': form,
        'formset': formset,
    }
    return render(request, 'Order/addMeasurement.html', context=context)
        

def get_garment_form(cloth_type, region, data=None):
    if region == 'upper':
        print(cloth_type)
        return UpperBodyForm(cloth_type=cloth_type, data=data)
    else:
        return LowerBodyForm(cloth_type=cloth_type, data=data)

def getGarmentByGender(gender):
    garments = []
    for name, attrs in GARMENT_TYPES.items():
        if attrs['gender'] == gender or attrs['gender'] == 'unisex':
            garments.append((name, attrs['region']))
    return garments

def getRegionByGarment(garment):
    for name, attrs in GARMENT_TYPES.items():
        if name == garment:
            return attrs['region']