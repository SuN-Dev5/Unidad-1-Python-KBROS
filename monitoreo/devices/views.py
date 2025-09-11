from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Device , Measurement , Zone , Category, Alert
from .forms import DeviceForm


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


def device_detail(request, pk):
    
    device = get_object_or_404(Device, pk=pk)
    
    return render(request, 'devices/device_detail.html', {'device': device})

def measurement_list(request):
    
    devices = Device.objects.select_related("category")
    
    return render(request, "devices/start.html", {"devices": devices})


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
    # Aquí iría la lógica de registro (crear usuario)
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