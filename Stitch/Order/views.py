from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from AuthApp.models import Customer
from Order.models import Order
from Cloth.forms import LowerBodyForm, LowerOptionsFormSet, UpperBodyForm, UpperOptionsFormSet
from .forms import OrderFormAddGarment
from Cloth.constants import GARMENT_TYPES


def home(request):
    from AuthApp.models import Customer

    orders = Order.objects.select_related('customer').order_by('-in_time')
    context = {
        'order_count': orders.count(),
        'urgent_count': orders.filter(status='Urgent').count(),
        'customer_count': Customer.objects.count(),
        'recent_orders': orders[:5],
    }
    return render(request, 'home.html', context)


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
    error = None
    if request.method == "POST":
        customer_id = request.POST.get('customer', '').strip()

        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
        else:
            name = request.POST.get('q', '').strip()
            phone = request.POST.get('phone', '').strip()
            if not name or not phone:
                error = "Select an existing customer, or enter a name and phone number to add a new one."
            else:
                customer, _ = Customer.objects.get_or_create(
                    phone=phone, defaults={'name': name}
                )

        if not error:
            gender_draft = request.session.get('gender_draft', {'gender': 'male'})
            request.session['draft_order'] = {
                'gender': gender_draft['gender'],
                'customer': customer.id,
            }
            return redirect('garmentPicker')

    search_query = request.GET.get('q', '').strip()
    customers_qs = Customer.objects.all().order_by('name')
    if search_query:
        customers_qs = customers_qs.filter(
            Q(name__icontains=search_query) | Q(phone__icontains=search_query)
        )
    paginator = Paginator(customers_qs, 8)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Live-search fetch from the frontend swaps just the results panel
    if request.GET.get('partial'):
        return render(request, 'Order/_customer_results.html', {
            'page_obj': page_obj, 'search_query': search_query,
        })

    context = {'page_obj': page_obj, 'search_query': search_query, 'error': error}
    return render(request, "Order/addOrder.html", context=context)

def garmentPicker(request):
    draft = request.session.get('draft_order',{})
    customer_name = Customer.objects.get(id = draft['customer'])
    garments = getGarmentByGender(draft['gender'])

    if request.method == 'POST':
        order = OrderFormAddGarment(request.POST)
        print(request.POST)
        if order.is_valid():
            obj = order.save(commit=False)
            obj.customer = customer_name
            obj.out_time = compute_out_time(obj.days)
            obj.save()

            request.session.pop('draft_order', None)
            request.session.pop('garment', None)
            request.session.pop('gender_draft', None)
            return redirect('home')
        else:
            print(order.errors)
            form = order
    else:
        draft_garment = request.session.get('garment',{})
        if draft_garment:
            draft[draft_garment['region']] = int(draft_garment['garment'])
        print(draft)
        form = OrderFormAddGarment(initial=draft)
    context = {
        'customer' : customer_name.name,
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

def cancelOrder(request):
    request.session.pop('draft_order', None)
    request.session.pop('garment', None)
    request.session.pop('gender_draft', None)
    return redirect('home')
        

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