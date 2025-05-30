from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Tipos de datos personalizados usando choices
class TipoRol(models.TextChoices):
    CLIENTE = 'cliente', 'Cliente'
    PREMIUM = 'premium', 'Cliente Premium'
    CORPORATIVO = 'corporativo', 'Cliente Corporativo'

class EstadoVenta(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    CONFIRMADA = 'confirmada', 'Confirmada'
    ENVIADA = 'enviada', 'Enviada'
    ENTREGADA = 'entregada', 'Entregada'
    CANCELADA = 'cancelada', 'Cancelada'

class Genero(models.Model):
    """Equivalente a Departamento en el diagrama original"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    """Equivalente a Profesor en el diagrama original"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    """Equivalente a Estudiante en el diagrama original"""
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField()
    fecha_nacimiento = models.DateField()
    tipo_cliente = models.CharField(
        max_length=20,
        choices=TipoRol.choices,
        default=TipoRol.CLIENTE
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    """Equivalente a Curso en el diagrama original"""
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    isbn = models.CharField(max_length=17, unique=True)
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.PositiveIntegerField(default=0)
    fecha_publicacion = models.DateField()
    paginas = models.PositiveIntegerField()
    genero = models.ForeignKey(
        Genero, 
        on_delete=models.CASCADE,
        related_name='libros'
    )
    autor_principal = models.ForeignKey(
        Autor,
        on_delete=models.CASCADE,
        related_name='libros_principales'
    )
    autores = models.ManyToManyField(Autor, related_name='libros_colaborativos')
    categorias = models.ManyToManyField(Categoria, related_name='libros')
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ['titulo']
    
    def __str__(self):
        return self.titulo

class Venta(models.Model):
    """Equivalente a Matrícula en el diagrama original - tabla intermedia"""
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    libro = models.ForeignKey(
        Libro,
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoVenta.choices,
        default=EstadoVenta.PENDIENTE
    )
    fecha_venta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    notas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_venta']
        # Restricción para evitar duplicados
        unique_together = ['cliente', 'libro', 'fecha_venta']
    
    def __str__(self):
        return f"Venta {self.id}: {self.cliente.nombre_completo} - {self.libro.titulo}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    @property
    def total_descuento(self):
        return (self.subtotal * self.descuento) / 100
    
    @property
    def total(self):
        return self.subtotal - self.total_descuento
    
    def save(self, *args, **kwargs):
        # Validación: el precio unitario no puede ser mayor al precio actual del libro
        if self.precio_unitario > self.libro.precio:
            raise ValueError("El precio unitario no puede ser mayor al precio actual del libro")
        super().save(*args, **kwargs)

class VistaLibroCompleta(models.Model):
    id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    isbn = models.CharField(max_length=13)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fecha_publicacion = models.DateField()
    paginas = models.IntegerField()
    genero = models.CharField(max_length=100)
    autor = models.CharField(max_length=255)

    class Meta:
        managed = False  # Django no intentará modificar esta vista
        db_table = 'vista_libros_completa'