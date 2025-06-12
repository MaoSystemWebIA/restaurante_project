from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Categoria, Producto, Mesa, Pedido, DetallePedido
from django.utils import timezone

# Create your views here.

@login_required
def menu(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'mi_app/menu.html', {
        'categorias': categorias,
        'productos': productos
    })

@login_required
def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'mi_app/lista_mesas.html', {'mesas': mesas})

@login_required
def crear_pedido(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    if request.method == 'POST':
        pedido = Pedido.objects.create(
            mesa=mesa,
            mesero=request.user,
            estado='pendiente'
        )
        mesa.estado = 'ocupada'
        mesa.save()
        return redirect('detalle_pedido', pedido_id=pedido.id)
    return render(request, 'mi_app/crear_pedido.html', {'mesa': mesa})

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Producto, id=producto_id)
        
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
        messages.success(request, 'Producto agregado al pedido')
        return redirect('detalle_pedido', pedido_id=pedido.id)
    
    productos = Producto.objects.filter(disponible=True)
    return render(request, 'mi_app/detalle_pedido.html', {
        'pedido': pedido,
        'productos': productos
    })

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    return render(request, 'mi_app/lista_pedidos.html', {'pedidos': pedidos})

@login_required
def actualizar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        
        if nuevo_estado == 'completado':
            pedido.mesa.estado = 'disponible'
            pedido.mesa.save()
        
        messages.success(request, 'Estado del pedido actualizado')
    return redirect('detalle_pedido', pedido_id=pedido.id)

@login_required
def eliminar_detalle_pedido(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    pedido_id = detalle.pedido.id
    detalle.delete()
    messages.success(request, 'Producto eliminado del pedido')
    return redirect('detalle_pedido', pedido_id=pedido_id)
