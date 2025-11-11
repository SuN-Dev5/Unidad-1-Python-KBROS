# productos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse  # 👈 ¡ESTA ES LA CORRECCIÓN!
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

# ---------------------------
# 📦 CRUD Productos
# ---------------------------

@login_required
@permission_required('productos.view_producto', raise_exception=True)
def producto_list(request):
    """
    Lista todos los productos. Exclusivo para Encargado EcoEnergy.
    """
    productos = Producto.objects.all().order_by('nombre')
    
    return render(request, 'productos/producto_list.html', {
        'productos': productos
    })

@login_required
@permission_required('productos.add_producto', raise_exception=True)
def producto_create(request):
    """
    Crea un nuevo producto.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm()
        
    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Crear Producto'
    })

@login_required
@permission_required('productos.change_producto', raise_exception=True)
def producto_update(request, pk):
    """
    Actualiza un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
        
    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': f'Editar {producto.nombre}'
    })

@login_required
@permission_required('productos.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    """
    Elimina un producto (usando SweetAlert).
    """
    # Esta vista es llamada por el script de SweetAlert que ya tenemos
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        try:
            producto.delete()
            return JsonResponse({'status': 'success', 'message': 'Producto eliminado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    # Si se accede por GET, no hacer nada
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)