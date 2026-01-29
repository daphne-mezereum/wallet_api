from .models import Wallet
from .serializers import WalletSerializer, WalletOperationSerializer
from .services import apply_wallet_operation
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status


class WalletDetailView(RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'uuid'


class WalletOperationView(CreateAPIView):
    serializer_class = WalletOperationSerializer

    def perform_create(self, serializer):
        apply_wallet_operation(
            wallet_uuid=self.kwargs["uuid"],
            operation_type=serializer.validated_data["operation_type"],
            amount=serializer.validated_data["amount"],
        )

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)
