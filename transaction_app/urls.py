from django.urls import path
from .views import WalletDetailView, WalletOperationView


urlpatterns = [
    path("wallets/<uuid:uuid>/", WalletDetailView.as_view(), name='wallet_detail'),
    path("wallets/<uuid:uuid>/operation", WalletOperationView.as_view(), name="wallet_operation"),
]
