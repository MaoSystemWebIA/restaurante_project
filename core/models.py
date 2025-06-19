from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrador')
        BUSINESS = 'BUSINESS', _('Negocio')
        SUPPORT = 'SUPPORT', _('Soporte')
        CUSTOMER = 'CUSTOMER', _('Cliente')

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to='business_logos/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_status = models.CharField(max_length=20, default='free')
    subscription_end_date = models.DateTimeField(null=True, blank=True)

class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True)
    is_active = models.BooleanField(default=True)

class Invoice(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='pending')

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

class Subscription(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, default='active')
    price = models.DecimalField(max_digits=10, decimal_places=2)

class KPI(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    customer_count = models.IntegerField() 