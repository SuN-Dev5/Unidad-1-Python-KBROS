from django.shortcuts import render , redirect
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
    
    devices = Device.objects.select_related("category")
    
    return render(request, "devices/start.html", {"devices": devices})

def measurement_list(request):
    
    devices = Device.objects.select_related("category")
    
    return render(request, "devices/start.html", {"devices": devices})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')

def register_view(request):
    # Aquí iría la lógica de registro (crear usuario)
    return render(request, 'register.html')
