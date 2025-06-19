from rest_framework import serializers
from .models import User, Business, Product, Invoice, InvoiceDetail, ChatMessage, Subscription, KPI

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'phone', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BusinessSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Business
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InvoiceDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True, read_only=True)
    customer = UserSerializer(read_only=True)
    business = BusinessSerializer(read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'

class KPISerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    
    class Meta:
        model = KPI
        fields = '__all__' 