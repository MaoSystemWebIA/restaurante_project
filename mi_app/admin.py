from django.contrib import admin
from .models import Categoria, Producto, Mesa, Pedido, DetallePedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidad', 'estado')
    list_filter = ('estado',)
    search_fields = ('numero',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'mesero', 'fecha', 'estado', 'total')
    list_filter = ('estado', 'fecha')
    search_fields = ('mesa__numero', 'mesero__username')

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('pedido__estado',)
    search_fields = ('producto__nombre', 'pedido__id')
