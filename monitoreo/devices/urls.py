# devices/urls.py
from django.urls import path
from . import views  # Importa las vistas de 'devices'

urlpatterns = [
    path('', views.start, name='start'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Devices
    path('devices/', views.device_list, name='device_list'),
    path('devices/create/', views.create_device, name='create_device'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('devices/<int:pk>/edit/', views.update_device, name='update_device'),
    path('devices/<int:pk>/delete/', views.delete_device, name='delete_device'),

    # RUTA DE EXPORTACIÓN AÑADIDA AQUÍ
    path('devices/export/excel/', views.export_devices_excel, name='export_devices_excel'),

    # Measurements
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/create/', views.create_measurement, name='create_measurement'),

    # Alerts
    path('alerts/add/', views.add_alert, name='add_alert'),
    path('alerts/add/<int:device_id>/', views.add_alert, name='add_alert_device'),
    path('alerts/summary/', views.alert_summary, name='alert_summary'),
]