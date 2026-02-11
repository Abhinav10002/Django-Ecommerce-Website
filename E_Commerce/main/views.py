from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from store_admin.models import Product, ContactMessage  


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def collections(request):
    products = Product.objects.all()
    return render(request, 'collections.html', {'products': products})


def submit_contact(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        
        ContactMessage.objects.create(name=name, email=email, message=message)

        
        subject = f"New Inquiry from {name}"
        body = f"""
        You have received a new message from the BikeGear Website.
        
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """

        
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,   
            [settings.EMAIL_HOST_USER], 
            fail_silently=False
        )

        
        messages.success(request, "Message sent successfully! We will contact you soon.")
        
        
        return redirect('/#contact') 

    return redirect('home')