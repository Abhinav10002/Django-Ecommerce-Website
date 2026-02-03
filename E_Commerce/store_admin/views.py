from django.shortcuts import *
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order


@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-ordered_date')
    return render(request, 'dashboard.html', {'orders': orders})

@staff_member_required
def update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.status == 'Pending':
        order.status = 'Accepted'
    elif order.status == 'Accepted':
        order.status = 'Packed'
    elif order.status == 'Packed':
        order.status = 'On The Way'
    elif order.status == 'On The Way':
        order.status = 'Delivered'
    
    order.save()
    return redirect('admin_dashboard')