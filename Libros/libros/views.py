from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import connection
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Venta, Cliente, Libro, Genero, Autor
from .forms import VentaForm, ClienteForm, LibroForm

def index(request):
    """Vista principal que usa la VIEW de la base de datos"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vista_ventas_completa")
        columns = [col[0] for col in cursor.description]
        ventas = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # Calcula el total de ingresos sumando el total de cada venta
    ingresos_totales = sum(float(venta['total']) for venta in ventas if 'total' in venta)

    return render(request, 'libros/index.html', {
        'ventas': ventas,
        'ingresos_totales': ingresos_totales,  
        'title': 'Sistema de Ventas de Libros'
    })

def venta_create(request):
    """Crear nueva venta con formulario master-detail"""
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            try:
                venta = form.save()
                messages.success(request, f'Venta #{venta.id} creada exitosamente.')
                return redirect('venta_detail', pk=venta.id)
            except Exception as e:
                messages.error(request, f'Error al crear la venta: {str(e)}')
    else:
        form = VentaForm()
    
    return render(request, 'libros/venta_form.html', {
        'form': form,
        'title': 'Nueva Venta',
        'action': 'Crear',
        'clientes': Cliente.objects.filter(activo=True).order_by('apellido', 'nombre'),
        'libros': Libro.objects.filter(activo=True, stock__gt=0).order_by('titulo'),
    })

def venta_detail(request, pk):
    """Detalle de una venta específica"""
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'libros/venta_detail.html', {
        'venta': venta,
        'title': f'Venta #{venta.id}'
    })

def venta_edit(request, pk):
    """Editar una venta existente"""
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            try:
                venta = form.save()
                messages.success(request, f'Venta #{venta.id} actualizada exitosamente.')
                return redirect('venta_detail', pk=venta.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar la venta: {str(e)}')
    else:
        form = VentaForm(instance=venta)
    
    return render(request, 'libros/venta_edit.html', {
        'form': form,
        'venta': venta,
        'title': f'Editar Venta #{venta.id}',
        'action': 'Actualizar',
        'clientes': Cliente.objects.filter(activo=True).order_by('apellido', 'nombre'),
        'libros': Libro.objects.filter(activo=True, stock__gt=0).order_by('titulo'),
    })

def venta_delete(request, pk):
    """Eliminar una venta"""
    venta = get_object_or_404(Venta, pk=pk)
    
    if request.method == 'POST':
        venta_id = venta.id
        venta.delete()
        messages.success(request, f'Venta #{venta_id} eliminada exitosamente.')
        return redirect('index')
    
    return render(request, 'libros/venta_confirm_delete.html', {
        'venta': venta,
        'title': f'Eliminar Venta #{venta.id}'
    })

def reporte_ventas(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vista_ventas_completa")
        columns = [col[0] for col in cursor.description]
        ventas = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(request, 'libros/reporte_ventas.html', {
        'ventas': ventas,
        'columnas': columns
    })

# CRUD para Cliente
def cliente_create(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre_completo} creado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    
    return render(request, 'libros/cliente_form.html', {
        'form': form,
        'title': 'Nuevo Cliente',
        'action': 'Crear'
    })

def cliente_list(request):
    """Lista de clientes"""
    clientes = Cliente.objects.filter(activo=True).order_by('apellido', 'nombre')
    return render(request, 'libros/cliente_list.html', {
        'clientes': clientes,
        'title': 'Lista de Clientes'
    })

def cliente_edit(request, pk):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre_completo} actualizado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'libros/cliente_form.html', {
        'form': form,
        'cliente': cliente,
        'title': f'Editar Cliente: {cliente.nombre_completo}',
        'action': 'Actualizar'
    })

# CRUD para Libro
def libro_create(request):
    """Crear nuevo libro"""
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('libro_list')
    else:
        form = LibroForm()
    
    autores = Autor.objects.filter(activo=True).order_by('apellido', 'nombre')
    generos = Genero.objects.filter(activo=True).order_by('nombre')
    
    return render(request, 'libros/libro_form.html', {
        'form': form,
        'title': 'Nuevo Libro',
        'action': 'Crear',
        'autores': autores,
        'generos': generos
    })

def libro_list(request):
    """Lista de libros"""
    libros = Libro.objects.filter(activo=True).select_related('autor_principal', 'genero').order_by('titulo')
    return render(request, 'libros/libro_list.html', {
        'libros': libros,
        'title': 'Lista de Libros'
    })

def libro_edit(request, pk):
    """Editar libro"""
    libro = get_object_or_404(Libro, pk=pk)
    
    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            libro = form.save()
            messages.success(request, f'Libro "{libro.titulo}" actualizado exitosamente.')
            return redirect('libro_list')
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'libros/libro_form.html', {
        'form': form,
        'libro': libro,
        'title': f'Editar Libro: {libro.titulo}',
        'action': 'Actualizar'
    })

# API para obtener precio de libro (para el formulario de ventas)
def get_libro_precio(request, libro_id):
    """API para obtener el precio actual de un libro"""
    try:
        libro = Libro.objects.get(id=libro_id)
        return JsonResponse({
            'precio': float(libro.precio),
            'stock': libro.stock,
            'titulo': libro.titulo
        })
    except Libro.DoesNotExist:
        return JsonResponse({'error': 'Libro no encontrado'}, status=404)

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'libros/cliente_list.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'libros/cliente_form.html', {'form': form})

def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'libros/cliente_form.html', {'form': form})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('cliente_list')

