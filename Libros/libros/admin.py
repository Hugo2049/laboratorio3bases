from django.contrib import admin
from .models import Genero, Autor, Cliente, Libro, Venta

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    ordering = ['nombre']

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'fecha_nacimiento', 'activo']
    list_filter = ['activo', 'fecha_nacimiento']
    search_fields = ['nombre', 'apellido', 'email']
    ordering = ['apellido', 'nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'tipo_cliente', 'fecha_registro', 'activo']
    list_filter = ['tipo_cliente', 'activo', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'email']
    ordering = ['apellido', 'nombre']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor_principal', 'genero', 'precio', 'stock', 'activo']
    list_filter = ['genero', 'activo', 'fecha_publicacion']
    search_fields = ['titulo', 'isbn', 'autor_principal__nombre', 'autor_principal__apellido']
    ordering = ['titulo']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'libro', 'cantidad', 'total', 'estado', 'fecha_venta']
    list_filter = ['estado', 'fecha_venta']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'libro__titulo']
    ordering = ['-fecha_venta']
    readonly_fields = ['fecha_venta', 'fecha_actualizacion']