from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from devices.views import (
    # Vistas principales
    start, dashboard,

    # Devices
    device_list, device_detail, create_device, update_device, delete_device,

    # Measurements
    measurement_list, create_measurement,

    # Alerts
    add_alert, alert_summary,

    # Auth & Profile
    login_view, logout_view, register_view, password_reset, edit_profile,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name='start'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Devices
    path('devices/', device_list, name='device_list'),
    path('devices/create/', create_device, name='create_device'),
    path('devices/<int:pk>/', device_detail, name='device_detail'),
    path('devices/<int:pk>/edit/', update_device, name='update_device'),
    path('devices/<int:pk>/delete/', delete_device, name='delete_device'),

    # Measurements
    path('measurements/', measurement_list, name='measurement_list'),
    path('measurements/create/', create_measurement, name='create_measurement'),

    # Alerts
    path('alerts/add/', add_alert, name='add_alert'),
    path('alerts/add/<int:device_id>/', add_alert, name='add_alert_device'),
    path('alerts/summary/', alert_summary, name='alert_summary'),

    # Auth & Profile
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('password_reset/', password_reset, name='password_reset'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
