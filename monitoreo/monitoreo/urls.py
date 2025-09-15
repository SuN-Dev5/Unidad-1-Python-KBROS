from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from devices.views import (
    start, create_device, logout_view, dashboard, device_list, measurement_list,
    login_view, register_view, device_detail, update_device, delete_device,
    edit_profile, password_reset, create_measurement
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name='start'),

    # Devices
    path('devices/', device_list, name='device_list'),
    path('devices/create/', create_device, name='create_device'),
    path('devices/<int:pk>/', device_detail, name='device_detail'),
    path('devices/<int:pk>/edit/', update_device, name='update_device'),
    path('devices/<int:pk>/delete/', delete_device, name='delete_device'),

    # Measurements
    path('measurements/', measurement_list, name='measurement_list'),
    path('measurements/create/', create_measurement, name='create_measurement'),

    # Auth & Profile
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('password_reset/', password_reset, name='password_reset'),
    path('profile/edit/', edit_profile, name='edit_profile'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
