from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from Order.models import Order



def checkout(request, id):
    order = get_object_or_404(
    Order.objects.prefetch_related(
        'tops__upper_body', 
        'bottoms__lower_body'
        ), 
        id=id
    )

    upperGarments = order.tops.all()
    bottomGarments = order.bottoms.all()

    context = {
        'order': order,
        'upperGarments': upperGarments,
        'bottomGarments': bottomGarments,
    }
    return render(request, 'Bill/bill.html', context=context)