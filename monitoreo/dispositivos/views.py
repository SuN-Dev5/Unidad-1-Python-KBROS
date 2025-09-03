from django.shortcuts import render
from .models import Dispositivo

def inicio(request):
    # dispositivos = Dispositivo.objects.all()
    dispositivos = Dispositivo.objects.select_related("categoria")  # join

    return render(request, "dispositivos/inicio.html", {"dispositivos": dispositivos})