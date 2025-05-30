from django import forms
from django.core.exceptions import ValidationError
from .models import Venta, Cliente, Libro, Genero, Autor, TipoRol, EstadoVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'libro', 'cantidad', 'precio_unitario', 'descuento', 'estado', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'libro': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
                'onchange': 'updatePrecio(this.value)'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'readonly': False
            }),
            'descuento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '0'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre la venta...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('apellido', 'nombre')
        # Filtrar solo libros activos con stock
        self.fields['libro'].queryset = Libro.objects.filter(activo=True, stock__gt=0).order_by('titulo')
        
        # Si estamos editando, prellenar el precio
        if self.instance and self.instance.pk:
            self.fields['precio_unitario'].initial = self.instance.libro.precio

    def clean(self):
        cleaned_data = super().clean()
        libro = cleaned_data.get('libro')
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')

        if libro and cantidad:
            # Validar stock disponible
            if cantidad > libro.stock:
                raise ValidationError(f'Stock insuficiente. Disponible: {libro.stock}')
            
            # Validar que el precio no sea mayor al precio actual del libro
            if precio_unitario and precio_unitario > libro.precio:
                raise ValidationError(f'El precio unitario no puede ser mayor al precio del libro (${libro.precio})')

        return cleaned_data

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'fecha_nacimiento', 'tipo_cliente']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa del cliente'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo_cliente': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar que el email no esté duplicado (excepto para el mismo cliente)
            existing = Cliente.objects.filter(email=email)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un cliente con este email.')
        
        return email

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'isbn', 'precio', 'stock', 'fecha_publicacion', 
                 'paginas', 'genero', 'autor_principal']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del libro'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción del libro...'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (13 dígitos)'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'fecha_publicacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'paginas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'genero': forms.Select(attrs={
                'class': 'form-control'
            }),
            'autor_principal': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo géneros y autores activos
        self.fields['genero'].queryset = Genero.objects.filter(activo=True).order_by('nombre')
        self.fields['autor_principal'].queryset = Autor.objects.filter(activo=True).order_by('apellido', 'nombre')

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            # Verificar que el ISBN no esté duplicado (excepto para el mismo libro)
            existing = Libro.objects.filter(isbn=isbn)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            
            if existing.exists():
                raise ValidationError('Ya existe un libro con este ISBN.')
            
            # Validar longitud del ISBN
            if len(isbn.replace('-', '').replace(' ', '')) != 13:
                raise ValidationError('El ISBN debe tener 13 dígitos.')
        
        return isbn