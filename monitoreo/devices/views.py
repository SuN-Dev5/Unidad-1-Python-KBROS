from django.shortcuts import render , redirect
from .models import Device
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