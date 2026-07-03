from django.utils import timezone
from datetime import timedelta

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
        request.session['gender_draft'] = {
            'gender':gender
        }
        return redirect('addOrder')
    return render(request, "Order/gender.html")
    
def addOrder(request):
    if request.method == 'POST':
        Customer = request.POST.get('customer')
        Upper = request.POST.get('upperBody')
        Lower = request.POST.get('lowerBody')
        status = request.POST.get('status')
        days = request.POST.get('days')
        outdate = request.POST.get('out_time')
        
        gender_draft = request.session.get('gender_draft',{'gender':'male'})

        request.session['draft_order'] = {
            'gender' : gender_draft['gender'],
            'customer' : int(Customer),
            'upperBody':Upper,
            'lowerBody':Lower,
            'status':status,
            'days':days,
            'out_time':outdate,
            } 

        return redirect('garmentPicker')
    
    form = OrderForm()
    return render(request,"Order/addOrder.html",{'form' : form})

def garmentPicker(request):
    draft = request.session.get('draft_order',{})
    garments = getGarmentByGender(draft['gender'])

    if request.method == 'POST':
        print("POST")
        order = OrderForm(request.POST)
        if order.is_valid():
            obj = order.save(commit=False)
            obj.out_time = compute_out_time(obj.days)
            obj.save()
            return redirect('home')
        else:
            print(order.errors)
            form = order
    else:
        draft_garment = request.session.get('garment',{})
        if draft_garment:
            draft[draft_garment['region']] = int(draft_garment['garment'])
        form = OrderForm(initial=draft)
        print(form)
    context = {
        'garments' : garments,
        'form' : form,
    }
    return render(request, 'Order/garment_picker.html', context=context)

def addCloth(request, cloth):
    region = getRegionByGarment(cloth)
    FormSetClass = UpperOptionsFormSet if region == 'upper' else LowerOptionsFormSet

    if request.method == 'POST':
        form = get_garment_form(cloth, region, data=request.POST)
        formset = FormSetClass(request.POST)
        if form.is_valid() and formset.is_valid():
            garment = form.save()             
            formset.instance = garment         
            formset.save()
            print(garment.id)
            request.session['garment'] = {
                'region' : 'upperBody' if region == 'upper' else 'lowerBody',
                'garment': garment.id,
            }               
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
        
def compute_out_time(days, placed_at=None):
    """
    Computes the promised pickup/completion time for an order.
    - days >= 1: noon, `days` days from when the order was placed.
    - days == 0 (rush order): 6pm today if that's still in the future,
      otherwise noon tomorrow (never returns a time in the past).
    """
    placed_at = placed_at or timezone.now()

    if days == 0:
        same_day_deadline = placed_at.replace(hour=18, minute=0, second=0, microsecond=0)
        if placed_at < same_day_deadline:
            return same_day_deadline
        return (placed_at + timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)

    base_noon = placed_at.replace(hour=12, minute=0, second=0, microsecond=0)
    return base_noon + timedelta(days=days)