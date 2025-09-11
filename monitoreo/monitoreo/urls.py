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
from devices.views import start, Device, create_device, dashboard, device_list, measurement_list, login_view, register_view, device_detail, update_device, delete_device, password_reset
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

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
    path('password_reset/', password_reset, name='password_reset'),
    path('<int:pk>/', device_detail, name='device_detail'),
    path('<int:pk>/edit/', update_device, name='update_device'),
    path('<int:pk>/delete/', delete_device, name='delete_device'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


