"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from devices.views import start, Device, create_device, dashboard, device_list, measurement_list, login_view, register_view, device_detail, update_device, delete_device
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name='start'),
    path('devices/<int:device_id>/', Device, name='device'),
    path('devices/create/', create_device, name='create_device'),
    path('dashboard/', dashboard, name='dashboard'),
    path('devices/', device_list, name='device_list'),
    path('measurement/', measurement_list, name='measurement_list'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('<int:pk>/', device_detail, name='device_detail'),
    path('<int:pk>/edit/', update_device, name='update_device'),
    path('<int:pk>/delete/', delete_device, name='delete_device'),

    #URLS para la recuparación de contraseña
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='devices/password_reset.html'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='devices/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='devices/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='devices/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

