from django.db import models
from django.conf import settings
from core.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Mesa(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]
    
    numero = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')

    def __str__(self):
        return f"Mesa {self.numero}"

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    mesero = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero}"
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        # Actualizar el total del pedido
        self.pedido.total = sum(detalle.subtotal for detalle in self.pedido.detalles.all())
        self.pedido.save()

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'



