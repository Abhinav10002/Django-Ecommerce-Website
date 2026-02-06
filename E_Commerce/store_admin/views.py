from django.shortcuts import *
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order


@staff_member_required
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-date')
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

def update_status(request, order_id):
    # 1. Find the specific order by its ID
    order = get_object_or_404(Order, id=order_id)
    
    # 2. Change status to True (Completed)
    order.status = True
    
    # 3. Save the change to the database
    order.save()
    
    # 4. Refresh the dashboard page
    return redirect('admin_dashboard')