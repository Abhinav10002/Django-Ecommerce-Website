import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone

from store_admin.models import Product, Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, "Account created! Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                
                otp = str(random.randint(100000, 999999))
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                
        
                try:
                    send_mail(
                        'Scam email',
                        f'Hello! Scammy this side your OTP for deducting 500$ from your account is: {otp}',
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False,
                    )
                except:
                    messages.error(request, "Error sending email.")
                
                return redirect('verify_otp')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        if stored_otp and user_otp == stored_otp:
            user = User.objects.get(id=user_id)
            login(request, user)
            del request.session['otp']
            del request.session['user_id']
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP.")
    return render(request, 'verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Create the order
    Order.objects.create(
        user=request.user,
        product=product,
        quantity=1,  
        price=product.price,
        date=timezone.now()
    )
    
    messages.success(request, "Order placed successfully!")
    return redirect('my_orders')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date')
    return render(request, 'my_orders.html', {'orders': orders})