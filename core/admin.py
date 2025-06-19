from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Business, Product, Invoice, InvoiceDetail, ChatMessage, Subscription, KPI

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('role', 'phone', 'address')}),
    )

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'subscription_status', 'created_at')
    list_filter = ('subscription_status', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'business')
    search_fields = ('name', 'description')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'customer', 'total', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('business__name', 'customer__username')

@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price')
    list_filter = ('invoice__business',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('content',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('business', 'plan', 'start_date', 'end_date', 'status')
    list_filter = ('plan', 'status')
    search_fields = ('business__name',)

@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    list_display = ('business', 'date', 'total_sales', 'total_orders', 'customer_count')
    list_filter = ('date', 'business')
    search_fields = ('business__name',) 