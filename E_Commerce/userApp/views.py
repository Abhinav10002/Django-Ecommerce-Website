import random
from django.shortcuts import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from store_admin.models import ContactMessage


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
                        'BikeGear',
                        f'OTP for BikeGear login: {otp}',
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


def request_otp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            otp = str(random.randint(100000, 999999))
            
            # Save data
            request.session['otp'] = otp
            request.session['otp_user_id'] = user.id
            request.session.save()  # <--- FORCE SAVE THE SESSION

            # Send Email
            print(f"DEBUG: Sending OTP {otp} to {user.email}") # Print to console to be sure
            
            subject = 'Your Login Verification Code'
            message = f"Hello {user.username},\n\nYour code is: {otp}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

            messages.success(request, f"OTP sent to {user.email}")
            return redirect('verify_otp')
        else:
            messages.error(request, "Username not found!")
    
    return render(request, 'request_otp.html')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        
        # Get data from session
        session_otp = request.session.get('otp')
        user_id = request.session.get('otp_user_id')

        # Debug Print - Look at your terminal for this!
        print(f"DEBUG CHECK: Session_OTP='{session_otp}' | Entered='{entered_otp}' | UserID='{user_id}'")

        if not session_otp or not user_id:
            messages.error(request, "Session expired (User ID missing). Please request a new OTP.")
            return redirect('request_otp')

        if str(entered_otp).strip() == str(session_otp).strip():
            # OTP Matches! Now try to get the user
            try:
                user = User.objects.get(id=user_id)
                login(request, user)
                
                # Cleanup
                del request.session['otp']
                del request.session['otp_user_id']
                
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, "User does not exist error.")
        else:
            messages.error(request, "Invalid OTP code.")

    return render(request, 'verify_otp.html')

def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 1. Save to Database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # 2. Send Email
        subject = f"New Inquiry from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False
        )

        messages.success(request, "Message sent successfully!")
        return redirect('/#contact') 

    return redirect('home')