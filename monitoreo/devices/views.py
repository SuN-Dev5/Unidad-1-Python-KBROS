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

from django.contrib import messages

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

    # Verificar si el usuario está autenticado
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
    

    # Últimas 10 mediciones de LA ORGANIZACIÓN

    latest_measurements = Measurement.objects.filter(
        organization=organization
    ).select_related('device').order_by('-date')[:10]
    

    # Alertas de la SEMANA actual por severidad
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # Conteo de alertas por severidad (esta semana)
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
    

    # Conteos para las tarjetas
    devices_count = Device.objects.filter(organization=organization).count()
    categories_count = Category.objects.filter(organization=organization).count()
    zones_count = Zone.objects.filter(organization=organization).count()


    return render(request, 'devices/dashboard.html', {
        'latest_measurements': latest_measurements,
        'recent_alerts': recent_alerts,
        'alert_counts': alert_counts,
        'devices_count': devices_count,

        'categories_count': categories_count,
        'zones_count': zones_count,
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
    

    measurements = Measurement.objects.filter(device=device).order_by('-date')[:10]
    alerts = Alert.objects.filter(device=device).order_by('-date')[:10]

    
    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    }
    
    return render(request, 'devices/device_detail.html', context)

def measurement_list(request):

    # Verificar autenticación y organización
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not hasattr(request.user, 'organization'):
        return redirect('dashboard')
    
    measurements = Measurement.objects.filter(
        organization=request.user.organization
    ).select_related('device', 'device__category', 'device__zone').order_by('-date')
    

    paginator = Paginator(measurements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'measurements': page_obj}
    return render(request, "devices/measurement_list.html", context)

def create_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            if hasattr(request.user, 'organization'):
                measurement.organization = request.user.organization
            measurement.save()
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


def add_alert(request, device_id=None):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    device = None
    if device_id:
        device = get_object_or_404(Device, id=device_id, organization=request.user.organization)
    
    if request.method == 'POST':
        device_id = request.POST.get('device')
        message = request.POST.get('message')
        severity = request.POST.get('severity')
        
        device = Device.objects.get(id=device_id, organization=request.user.organization)
        
        Alert.objects.create(
            device=device,
            message=message,
            severity=severity,
            organization=request.user.organization
        )
        
        if device_id:
            return redirect('device_detail', pk=device_id)
        return redirect('alert_summary')
    
    devices = Device.objects.filter(organization=request.user.organization)
    
    return render(request, 'devices/alert_form.html', {
        'devices': devices,
        'device': device,
        'title': 'Agregar Alerta' if not device else f'Agregar Alerta para {device.name}'
    })

# ✅ HU5 - ALERT SUMMARY
def alert_summary(request):

    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not hasattr(request.user, 'organization') or not request.user.organization:
        return redirect('dashboard')
    
    organization = request.user.organization
    one_week_ago = timezone.now() - timedelta(days=7)
    


    alerts = Alert.objects.filter(
        organization=organization,
        date__gte=one_week_ago
    ).select_related('device').order_by('-date')
    


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


def measurement_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    measurement = get_object_or_404(Measurement, pk=pk, organization=request.user.organization)
    
    if request.method == 'POST':
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            return redirect('measurement_list')
    else:
        form = MeasurementForm(instance=measurement)
    
    return render(request, 'devices/measurement_form.html', {
        'form': form,
        'title': 'Editar Medición',
        'measurement': measurement
    })

# ✅ HU9 - DELETE MEASUREMENT
def measurement_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    measurement = get_object_or_404(Measurement, pk=pk, organization=request.user.organization)
    
    if request.method == 'POST':
        measurement.delete()
        return redirect('measurement_list')
    
    return render(request, 'devices/measurement_confirm_delete.html', {
        'measurement': measurement
    })

# ✅ HU12 - EDIT ORGANIZATION
def edit_organization(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    if not hasattr(request.user, 'organization') or not request.user.organization:
        return redirect('dashboard')
    
    organization = request.user.organization
    
    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_status = request.POST.get('status')
        
        organization.name = new_name
        organization.status = new_status
        organization.save()
        
        messages.success(request, 'Organización actualizada correctamente')
        return redirect('dashboard')
    
    return render(request, 'devices/organization_form.html', {
        'organization': organization,
        'title': 'Editar Organización'
    })

