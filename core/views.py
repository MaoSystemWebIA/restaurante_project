from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Business, Product, Invoice, InvoiceDetail, ChatMessage, Subscription, KPI
from .serializers import (
    UserSerializer, BusinessSerializer, ProductSerializer,
    InvoiceSerializer, InvoiceDetailSerializer, ChatMessageSerializer,
    SubscriptionSerializer, KPISerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Business.objects.all()
        return Business.objects.filter(user=self.request.user)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Product.objects.all()
        return Product.objects.filter(business__user=self.request.user)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Invoice.objects.all()
        elif self.request.user.role == 'BUSINESS':
            return Invoice.objects.filter(business__user=self.request.user)
        return Invoice.objects.filter(customer=self.request.user)

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(
            sender=self.request.user
        ) | ChatMessage.objects.filter(
            receiver=self.request.user
        )

    @action(detail=False, methods=['get'])
    def unread(self, request):
        messages = self.get_queryset().filter(receiver=request.user, is_read=False)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Subscription.objects.all()
        return Subscription.objects.filter(business__user=self.request.user)

class KPIViewSet(viewsets.ModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return KPI.objects.all()
        return KPI.objects.filter(business__user=self.request.user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        business = get_object_or_404(Business, user=request.user)
        kpis = KPI.objects.filter(business=business).order_by('-date')[:30]
        serializer = self.get_serializer(kpis, many=True)
        return Response(serializer.data) 