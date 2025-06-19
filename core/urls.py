from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, BusinessViewSet, ProductViewSet,
    InvoiceViewSet, ChatMessageViewSet, SubscriptionViewSet,
    KPIViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'messages', ChatMessageViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'kpis', KPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 