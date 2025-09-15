from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils.timezone import now
from datetime import timedelta

from .models import Device, Measurement, Zone, Category, Alert, Organization
from .forms import DeviceForm, UserUpdateForm, MeasurementForm, AlertForm


# ---------------------------
# 🔐 Autenticación
# ---------------------------

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'devices/login.html', {
                'error': 'Email o contraseña incorrectos'
            })
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
            # 🔹 Crear organización asociada al usuario
            Organization.objects.create(name=company_name)

            return render(request, 'devices/register.html', {
                'success': f'¡Registro exitoso! La empresa {company_name} ha sido registrada correctamente.'
            })
        except IntegrityError:
            return render(request, 'devices/register.html', {
                'error': 'Este correo electrónico ya está registrado'
            })
        except Exception:
            return render(request, 'devices/register.html', {
                'error': 'Error al registrar la empresa. Intenta nuevamente.'
            })

    return render(request, 'devices/register.html')


def password_reset(request):
    message_sent = False
    if request.method == "POST":
        email = request.POST.get('email')
        message_sent = True
    return render(request, 'devices/password_reset.html', {'message_sent': message_sent})


@login_required
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


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------------------
# 📊 Dashboard
# ---------------------------

@login_required
def dashboard(request):
    latest_measurements = Measurement.objects.order_by('-date')[:10]
    recent_alerts = Alert.objects.order_by('-date')[:5]

    alert_count = Alert.objects.count()
    categories = Category.objects.all()
    zones = Zone.objects.all()
    devices = Device.objects.all()
    devices_count = devices.count()

    # Resumen de alertas por severidad (última semana)
    one_week_ago = now() - timedelta(days=7)
    alerts_week = Alert.objects.filter(date__gte=one_week_ago)

    alert_counts = {
        'high': alerts_week.filter(severity='high').count(),
        'medium': alerts_week.filter(severity='medium').count(),
        'low': alerts_week.filter(severity='low').count(),
    }

    from .models import Organization
    organization = Organization.objects.first()  

    return render(request, 'devices/dashboard.html', {
        'latest_measurements': latest_measurements,
        'recent_alerts': recent_alerts,
        'alert_count': alert_count,
        'categories': categories,
        'zones': zones,
        'devices': devices,
        'devices_count': devices_count,
        'alert_counts': alert_counts,
        'organization': organization,   
    })



# ---------------------------
# 💻 Dispositivos
# ---------------------------

@login_required
def device_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')

    devices = Device.objects.select_related("category", "zone")
    if selected_category:
        devices = devices.filter(category_id=selected_category)

    return render(request, "devices/device.html", {
        "devices": devices,
        "categories": categories,
        "selected_category": selected_category,
    })


@login_required
def device_detail(request, pk):
    device = get_object_or_404(Device, pk=pk)
    measurements = Measurement.objects.filter(device=device).order_by('-date')[:10]
    alerts = Alert.objects.filter(device=device).order_by('-date')[:10]

    return render(request, 'devices/device_detail.html', {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    })


@login_required
def create_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('device_list')
    else:
        form = DeviceForm()
    return render(request, 'devices/create.html', {'form': form})


@login_required
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


@login_required
def delete_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'devices/delete_device.html', {'device': device})


# ---------------------------
# 📏 Mediciones
# ---------------------------

@login_required
def measurement_list(request):
    measurements = Measurement.objects.select_related('device', 'device__category', 'device__zone').order_by('-date')

    from django.core.paginator import Paginator
    paginator = Paginator(measurements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "devices/measurement_list.html", {"measurements": page_obj})


@login_required
def create_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('measurement_list')
    else:
        form = MeasurementForm()
    return render(request, 'devices/create_measurement.html', {'form': form})


# ---------------------------
# 🚨 Alertas
# ---------------------------

@login_required
def add_alert(request, device_id=None):
    devices = Device.objects.all()
    device = None

    if device_id:
        device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        device_id = request.POST.get('device') or (device.id if device else None)
        message = request.POST.get('message')
        severity = request.POST.get('severity')

        if device_id and message and severity:
            device_obj = get_object_or_404(Device, id=device_id)
            Alert.objects.create(
                device=device_obj,
                message=message,
                severity=severity,
                organization=device_obj.organization
            )
            return redirect('dashboard')

    return render(request, 'devices/alert_form.html', {
        'devices': devices,
        'device': device
    })



@login_required
def alert_summary(request):
    week_ago = now() - timedelta(days=7)
    alerts = Alert.objects.filter(date__gte=week_ago).order_by('-date')

    alert_counts = {
        'high': alerts.filter(severity='high').count(),
        'medium': alerts.filter(severity='medium').count(),
        'low': alerts.filter(severity='low').count(),
    }

    from .models import Organization
    organization = Organization.objects.first()

    return render(request, 'devices/alert_summary.html', {
        'alerts': alerts,
        'alert_counts': alert_counts,
        'one_week_ago': week_ago,
        'organization': organization,   
    })




# ---------------------------
# 🌐 Página inicial
# ---------------------------

def start(request):
    devices = Device.objects.select_related("category")
    return render(request, "devices/start.html", {"devices": devices})
