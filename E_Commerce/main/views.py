from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from store_admin.models import Product, ContactMessage  # Import your models

# Home Page View
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Collections Page View
def collections(request):
    products = Product.objects.all()
    return render(request, 'collections.html', {'products': products})

# Contact Form Submission View
def submit_contact(request):
    if request.method == 'POST':
        # 1. Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # 2. Save to Database (Backup)
        ContactMessage.objects.create(name=name, email=email, message=message)

        # 3. Send Email to Admin (You)
        subject = f"New Inquiry from {name}"
        body = f"""
        You have received a new message from the BikeGear Website.
        
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """

        # Sends the email
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,   # From (Your Gmail)
            [settings.EMAIL_HOST_USER], # To (Your Gmail)
            fail_silently=False
        )

        # 4. Success Message & Redirect
        messages.success(request, "Message sent successfully! We will contact you soon.")
        
        # This redirects back to the 'Contact' section of the home page
        return redirect('/#contact') 

    return redirect('home')