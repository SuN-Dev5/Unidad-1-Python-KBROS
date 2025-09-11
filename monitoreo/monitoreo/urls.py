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
from django.contrib import admin
from django.urls import path

from devices.views import start, Device, create_device, dashboard, device_list , measurement_list, login_view , register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name="start"),
    path('devices/<int:device_id>/', Device, name="device"),
    path('devices/create/',create_device, name="create_device"),
    path('dashboard/', dashboard, name='dashboard'),
    path('devices/', device_list, name='device_list'),
    path('measurement/', measurement_list, name='measurement_list'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]