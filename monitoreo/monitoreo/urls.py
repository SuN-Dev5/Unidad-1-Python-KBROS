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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from devices.views import (
    start, device_detail, create_device, dashboard, device_list, measurement_list, 
    login_view, register_view, update_device, delete_device, 
    edit_profile, password_reset, create_measurement,
    # ✅ NUEVAS VIEWS PARA LAS HU
    alert_summary, measurement_edit, measurement_delete, add_alert, edit_organization
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name='start'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password_reset/', password_reset, name='password_reset'),
    
    # Devices URLs
    path('devices/', device_list, name='device_list'),
    path('devices/create/', create_device, name='create_device'),
    path('devices/<int:pk>/', device_detail, name='device_detail'),
    path('devices/<int:pk>/edit/', update_device, name='update_device'),
    path('devices/<int:pk>/delete/', delete_device, name='delete_device'),
    
    # Measurements URLs
    path('measurements/', measurement_list, name='measurement_list'),
    path('measurements/create/', create_measurement, name='create_measurement'),
    path('measurements/<int:pk>/edit/', measurement_edit, name='measurement_edit'),
    path('measurements/<int:pk>/delete/', measurement_delete, name='measurement_delete'),
    
    # Profile URLs
    path('profile/edit/', edit_profile, name='edit_profile'),
    
    # ✅ NUEVAS URLs PARA LAS HU
    # HU5 - Resumen de alertas de la semana
    path('alerts/summary/', alert_summary, name='alert_summary'),
    
    # HU13 - Add Alert
    path('alerts/add/', add_alert, name='add_alert'),
    path('devices/<int:device_id>/add-alert/', add_alert, name='add_alert_device'),
    
    # HU12 - Edit Organization
    path('organization/edit/', edit_organization, name='edit_organization'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)