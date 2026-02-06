from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store_admin import views as admin_views

# Import views from your apps
from main import views as main_views
from userApp import views as user_views
from store_admin import views as admin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('collections/', main_views.collections, name='collections'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('buy/<int:product_id>/', user_views.place_order, name='place_order'),
    path('my-orders/', user_views.my_orders, name='my_orders'),
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('update-order/<int:order_id>/', admin_views.update_status, name='update_status'),
    path('verify-otp/', user_views.verify_otp, name='verify_otp'),
    path('update-status/<int:order_id>/', admin_views.update_status, name='update_status'),
    path('login-otp/', user_views.request_otp, name='request_otp'),  
    path('verify-otp/', user_views.verify_otp, name='verify_otp'),
    path('submit-contact/', user_views.submit_contact, name='submit_contact'),    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
