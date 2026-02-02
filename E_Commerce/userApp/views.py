from django.shortcuts import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from store_admin.models import Product
from .models import Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(
        user=request.user,
        product=product,
        quantity=1
    )
    return redirect('my_orders')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'my_orders.html', {'orders': orders})