from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Device, Measurement, Zone, Category, Alert, Organization  
from .forms import DeviceForm, UserUpdateForm, MeasurementForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def start(request):
    devices = Device.objects.select_related("category")
    return render(request, "devices/start.html", {"devices": devices})

def device(request, device_id):
    device = Device.objects.get(id=device_id)
    return render(request, "devices/device.html", {"device": device})

def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_device')
    else:
        form = DeviceForm()
    return render(request, 'devices/create.html', {'form': form})

def dashboard(request):
    #  VERIFICACIÓN DE AUTENTICACIÓN Y ORGANIZACIÓN
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not hasattr(request.user, 'organization') or not request.user.organization:
        # Crear organización demo si no existe
        organization, created = Organization.objects.get_or_create(
            name=f"Organización de {request.user.first_name or 'Demo'}"
        )
        request.user.organization = organization
        request.user.save()
    
    organization = request.user.organization
    
    # Últimas 10 mediciones
    latest_measurements = Measurement.objects.filter(
        organization=organization
    ).select_related('device').order_by('-date')[:10]
    
    # Alertas de la semana (últimos 7 días)
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # Conteo de alertas por severidad
    alert_counts = {
        'high': Alert.objects.filter(
            organization=organization,
            date__gte=one_week_ago,
            severity='high'
        ).count(),
        'medium': Alert.objects.filter(
            organization=organization,
            date__gte=one_week_ago,
            severity='medium'
        ).count(),
        'low': Alert.objects.filter(
            organization=organization,
            date__gte=one_week_ago,
            severity='low'
        ).count(),
    }
    
    # Alertas recientes (esta semana)
    recent_alerts = Alert.objects.filter(
        organization=organization,
        date__gte=one_week_ago
    ).select_related('device').order_by('-date')[:5]
    
    # Conteos generales
    devices_count = Device.objects.filter(organization=organization).count()
    categories = Category.objects.filter(organization=organization).annotate(
        device_count=Count('device')
    )
    zones = Zone.objects.filter(organization=organization).annotate(
        device_count=Count('device')
    )

    return render(request, 'devices/dashboard.html', {
        'latest_measurements': latest_measurements,
        'recent_alerts': recent_alerts,
        'alert_counts': alert_counts,
        'devices_count': devices_count,
        'categories': categories,
        'zones': zones,
    })

def device_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')
    devices = Device.objects.select_related("category", "zone")

    if selected_category:
        devices = devices.filter(category_id=selected_category)

    context = {
        "devices": devices,
        "categories": categories,
        "selected_category": selected_category,
    }
    return render(request, "devices/device.html", context)

@login_required
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    
    measurements = Measurement.objects.filter(
        device=device
    ).order_by('-date')[:10]
    
    alerts = Alert.objects.filter(
        device=device
    ).order_by('-date')[:10]
    
    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    }
    
    return render(request, 'devices/device_detail.html', context)

def measurement_list(request):
    measurements = Measurement.objects.select_related('device', 'device__category', 'device__zone').order_by('-date')
    
    from django.core.paginator import Paginator
    paginator = Paginator(measurements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'measurements': page_obj,
    }
    
    return render(request, "devices/measurement_list.html", context)

def create_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('measurement_list')
    else:
        form = MeasurementForm()
    return render(request, 'devices/create_measurement.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'devices/login.html', {'error': 'Email o contraseña incorrectos'})
    return render(request, 'devices/login.html')

def register_view(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            return render(request, 'devices/register.html', {
                'error': 'Las contraseñas no coinciden'
            })
        
        if len(password) < 12:
            return render(request, 'devices/register.html', {
                'error': 'La contraseña debe tener al menos 12 caracteres'
            })
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=company_name
            )
            
            # ✅ CREAR ORGANIZACIÓN AUTOMÁTICAMENTE AL REGISTRARSE
            organization = Organization.objects.create(name=company_name)
            user.organization = organization
            user.save()
            
            return render(request, 'devices/register.html', {
                'success': f'¡Registro exitoso! La empresa {company_name} ha sido registrada correctamente.'
            })
            
        except IntegrityError:
            return render(request, 'devices/register.html', {
                'error': 'Este correo electrónico ya está registrado'
            })
        
        except Exception as e:
            return render(request, 'devices/register.html', {
                'error': 'Error al registrar la empresa. Intenta nuevamente.'
            })
    
    return render(request, 'devices/register.html')


def update_device(request, pk):
    
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)

    return render(request, 'devices/update_device.html', {'form': form, 'device': device})

def delete_device(request, pk):
    
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('list_device')

    return render(request, 'devices/delete_confirm.html', {'device': device})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'devices/edit_profile.html', {'form': form})
  
def password_reset(request):
    message_sent = False

    if request.method == "POST":
        email = request.POST.get('email')
        message_sent = True

    return render(request, 'devices/password_reset.html', {'message_sent': message_sent})


def alert_summary(request):
    # Verificar autenticación
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not hasattr(request.user, 'organization') or not request.user.organization:
        return redirect('dashboard')
    
    organization = request.user.organization
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # Alertas de la semana
    alerts = Alert.objects.filter(
        organization=organization,
        date__gte=one_week_ago
    ).select_related('device').order_by('-date')
    
    # Conteo por severidad
    alert_counts = {
        'high': alerts.filter(severity='high').count(),
        'medium': alerts.filter(severity='medium').count(),
        'low': alerts.filter(severity='low').count(),
    }
    
    return render(request, 'devices/alert_summary.html', {
        'alerts': alerts,
        'alert_counts': alert_counts,
        'one_week_ago': one_week_ago,
    })

