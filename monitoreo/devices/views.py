from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import Device , Measurement , Zone , Category, Alert
from .forms import DeviceForm, UserUpdateForm, MeasurementForm
from django.contrib.auth.decorators import login_required

def start(request):
    # dispositivos = Dispositivo.objects.all()
    devices = Device.objects.select_related("category")  # join

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
    latest_measurements = Measurement.objects.order_by('-date')[:10]
    recent_alerts = Alert.objects.order_by('-date')[:5]
    alert_count = Alert.objects.count()  # 👉 muestra todas las alertas, sin filtrar por semana

    categories = Category.objects.all()
    zones = Zone.objects.all()
    devices = Device.objects.all()

    return render(request, 'devices/dashboard.html', {
        'latest_measurements': latest_measurements,
        'recent_alerts': recent_alerts,
        'alert_count': alert_count,
        'categories': categories,
        'zones': zones,
        'devices': devices
    })
    
def device_list(request):
    categories = Category.objects.all()  # Obtener todas las categorías para el filtro

    selected_category = request.GET.get('category', '')  # Obtener categoría seleccionada (vacío si no hay)

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
    
    # Obtener mediciones ordenadas por fecha descendente
    measurements = Measurement.objects.filter(
        device=device
    ).order_by('-date')[:10]  # Últimas 10 mediciones
    
    # Obtener alertas del dispositivo ordenadas por fecha descendente
    alerts = Alert.objects.filter(
        device=device
    ).order_by('-date')[:10]  # Últimas 10 alertas
    
    context = {
        'device': device,
        'measurements': measurements,
        'alerts': alerts,
    }
    
    return render(request, 'devices/device_detail.html', context)

def measurement_list(request):
    # Obtener todas las mediciones ordenadas descendentemente por fecha
    measurements = Measurement.objects.select_related('device', 'device__category', 'device__zone').order_by('-date')
    
    # Paginación simple (máximo 50 registros)
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
    
    # Caso GET: cuando alguien visita la página por primera vez
    return render(request, 'devices/login.html')

def register_view(request):
  
    if request.method == 'POST':
        company_name = request.POST['company_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # Validar que las contraseñas coincidan
        if password != password_confirm:
            return render(request, 'devices/register.html', {
                'error': 'Las contraseñas no coinciden'
            })
        
        # Validar longitud de contraseña
        if len(password) < 12:
            return render(request, 'devices/register.html', {
                'error': 'La contraseña debe tener al menos 12 caracteres'
            })
        
        try:
            # Crear usuario usando email como username
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=company_name
            )
            
            # Mensaje de éxito
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
    
    # Caso GET: mostrar formulario
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
    # Verificar autenticación
    if not request.user.is_authenticated:
        return redirect('login_view')
    
    device = None
    if device_id:
        device = get_object_or_404(Device, id=device_id, organization=request.user.organization)
    
    if request.method == 'POST':
        # Crear alerta manualmente desde el formulario
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
    
    # Si es GET, mostrar formulario
    devices = Device.objects.filter(organization=request.user.organization)
    
    return render(request, 'devices/alert_form.html', {
        'devices': devices,
        'device': device,
        'title': 'Agregar Alerta' if not device else f'Agregar Alerta para {device.name}'
    })
