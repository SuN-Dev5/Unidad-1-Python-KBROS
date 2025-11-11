# devices/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q                        
from django.http import JsonResponse                 
from django.contrib import messages 
from django.http import HttpResponse, JsonResponse # Añade HttpResponse
from django.db.models import Q
import openpyxl # Importa la librería                 

# Importamos solo los modelos y forms de ESTA app
from .models import Device, Measurement, Zone, Category, Alert, Organization
from .forms import DeviceForm, MeasurementForm, AlertForm

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

    one_week_ago = now() - timedelta(days=7) # 👈 Esta es la línea que faltaba
    
    alerts_week = Alert.objects.filter(date__gte=one_week_ago) # Ahora 'one_week_ago' está definida

    alert_counts = {
        'high': alerts_week.filter(severity='high').count(),
        'medium': alerts_week.filter(severity='medium').count(),
        'low': alerts_week.filter(severity='low').count(),
    }

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
# 💻 Dispositivos (CRUD 1)
# ---------------------------

@login_required
def device_list(request):
    
    # 👈 NUEVO: Lógica de Búsqueda (Rúbrica)
    if 'search' in request.GET:
        search_query = request.GET.get('search', '')
        request.session['device_search'] = search_query
    else:
        search_query = request.session.get('device_search', '')

    # 👈 NUEVO: Lógica de Paginador (Rúbrica)
    if 'page_size' in request.GET:
        page_size = request.GET.get('page_size', '5')
        request.session['device_page_size'] = page_size
    else:
        page_size = request.session.get('device_page_size', '5')
    
    try:
        page_size_int = int(page_size)
    except ValueError:
        page_size_int = 5
        
    # --- Tu lógica de filtrado original ---
    devices = Device.objects.select_related("category", "zone").order_by('name')
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')

    if selected_category:
        devices = devices.filter(category_id=selected_category)
    
    # 👈 NUEVO: Aplicar filtro de búsqueda
    if search_query:
        devices = devices.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(zone__name__icontains=search_query)
        )

    # 👈 NUEVO: Aplicar paginador con tamaño variable
    paginator = Paginator(devices, page_size_int)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "devices/device.html", {
        "devices": page_obj,  # 👈 MODIFICADO: Pasamos el 'page_obj'
        "categories": categories,
        "selected_category": selected_category,
        "search_query": search_query,      # 👈 NUEVO: Devolvemos valores
        "selected_page_size": page_size, # 👈 NUEVO: Devolvemos valores
    })


@login_required
def device_detail(request, pk):
    # ... (Esta vista estaba perfecta) ...
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
        form = DeviceForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo creado exitosamente.') # 👈 NUEVO
            return redirect('device_list')
    else:
        form = DeviceForm()
    # Recomiendo renombrar 'create.html' a 'device_form.html' y usarlo para crear y editar
    return render(request, 'devices/create.html', {'form': form})


@login_required
def update_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        form = DeviceForm(request.POST, request.FILES or None, instance=device)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dispositivo actualizado exitosamente.') # 👈 NUEVO
            return redirect('device_detail', pk=device.pk)
    else:
        form = DeviceForm(instance=device)
    # Recomiendo usar el template 'device_form.html' también aquí
    return render(request, 'devices/update_device.html', {'form': form, 'device': device}) 


@login_required
def delete_device(request, pk):
    # 👈 MODIFICADO: Para SweetAlert2
    device = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        try:
            device.delete()
            # No usamos messages aquí porque la página se recargará vía JS
            return JsonResponse({'status': 'success', 'message': 'Dispositivo eliminado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Si se accede por GET, no hacer nada (o devolver error)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


# ---------------------------
# 📏 Mediciones (CRUD 2 - Parcial)
# ---------------------------

@login_required
def measurement_list(request):
    # 👈 MODIFICADO: Aplicamos la misma lógica de búsqueda y paginador
    
    if 'search' in request.GET:
        search_query = request.GET.get('search', '')
        request.session['measurement_search'] = search_query
    else:
        search_query = request.session.get('measurement_search', '')

    if 'page_size' in request.GET:
        page_size = request.GET.get('page_size', '10') # Default 10 aquí
        request.session['measurement_page_size'] = page_size
    else:
        page_size = request.session.get('measurement_page_size', '10')
    
    try:
        page_size_int = int(page_size)
    except ValueError:
        page_size_int = 10

    measurements_all = Measurement.objects.select_related('device', 'device__category', 'device__zone').order_by('-date')
    
    if search_query:
        # Buscamos por nombre de dispositivo o valor de consumo
        q_lookup = Q(device__name__icontains=search_query)
        try:
            # Intentar buscar por valor numérico
            search_float = float(search_query)
            q_lookup |= Q(consumption=search_float)
        except ValueError:
            pass # Si no es un número, solo busca por nombre
            
        measurements_all = measurements_all.filter(q_lookup)

    paginator = Paginator(measurements_all, page_size_int)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "devices/measurement_list.html", {
        "measurements": page_obj,
        "search_query": search_query,
        "selected_page_size": page_size,
    })


@login_required
def create_measurement(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medición registrada exitosamente.') # 👈 NUEVO
            return redirect('measurement_list')
    else:
        form = MeasurementForm()
    return render(request, 'devices/create_measurement.html', {'form': form})


# ---------------------------
# 🚨 Alertas (CRUD 3 - Parcial)
# ---------------------------

@login_required
def add_alert(request, device_id=None):
    # 👈 MODIFICADO: Para usar el AlertForm que ya existe
    
    device = None
    initial_data = {}
    if device_id:
        device = get_object_or_404(Device, id=device_id)
        initial_data['device'] = device
        # Asumimos que la organización es la del dispositivo
        if device.organization:
             initial_data['organization'] = device.organization

    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alerta creada exitosamente.') # 👈 NUEVO
            return redirect('dashboard')
    else:
        # Pasamos los datos iniciales (el dispositivo pre-seleccionado)
        form = AlertForm(initial=initial_data)

    return render(request, 'devices/alert_form.html', {
        'form': form,      # 👈 MODIFICADO
        'device': device
    })


@login_required
def alert_summary(request):
    # ... (Esta vista estaba perfecta) ...
    week_ago = now() - timedelta(days=7)
    alerts = Alert.objects.filter(date__gte=week_ago).order_by('-date')
    alert_counts = {
        'high': alerts.filter(severity='high').count(),
        'medium': alerts.filter(severity='medium').count(),
        'low': alerts.filter(severity='low').count(),
    }
    organization = Organization.objects.first()
    return render(request, 'devices/alert_summary.html', {
        'alerts': alerts,
        'alert_counts': alert_counts,
        'one_week_ago': week_ago,
        'organization': organization,  
    })

# ---------------------------
# 🌐 Página inicial (No logueado)
# ---------------------------

def start(request):
    # ... (Esta vista estaba perfecta) ...
    devices = Device.objects.select_related("category")
    return render(request, "devices/start.html", {"devices": devices})


# ---------------------------
# ⬇️ Exportación a Excel (Rúbrica)
# ---------------------------
@login_required
def export_devices_excel(request):
    """
    Genera un archivo Excel (.xlsx) con la lista de dispositivos.
    """
    # Obtenemos los dispositivos (podríamos aplicar los filtros de sesión si quisiéramos)
    devices = Device.objects.select_related("category", "zone").order_by('name')

    # 1. Crear el libro de trabajo (Workbook)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dispositivos"

    # 2. Definir los encabezados (Rúbrica pide encabezados)
    headers = ["ID", "Nombre", "Categoría", "Zona", "Consumo Máx. (W)", "Estado"]
    ws.append(headers)

    # 3. Añadir los datos
    for device in devices:
        ws.append([
            device.id,
            device.name,
            device.category.name if device.category else "N/A",
            device.zone.name if device.zone else "N/A",
            device.maximum_consumption,
            device.get_status_display() # 'get_status_display' obtiene el texto legible (ej. "Active")
        ])

    # 4. Configurar la respuesta HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="dispositivos.xlsx"'

    # 5. Guardar el libro en la respuesta
    wb.save(response)

    return response