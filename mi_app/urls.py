from django.urls import path
from . import views

app_name = 'mi_app'

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesas/<int:mesa_id>/crear-pedido/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/<int:pedido_id>/actualizar-estado/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('pedidos/detalle/<int:detalle_id>/eliminar/', views.eliminar_detalle_pedido, name='eliminar_detalle_pedido'),
] 