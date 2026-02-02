from django.shortcuts import *
from store_admin.models import Product  

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def collections(request):
    products = Product.objects.all()
    return render(request, 'collections.html', {'products': products})