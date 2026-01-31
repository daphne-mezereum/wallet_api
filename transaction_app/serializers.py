from rest_framework import serializers
from decimal import Decimal
from .models import Wallet
from .services import Operations


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uuid', 'balance']
        read_only_fields = ["uuid", "balance"]


class WalletOperationSerializer(serializers.Serializer):
    operation_type = serializers.ChoiceField(choices=[Operations.deposit, Operations.withdraw])
    amount = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
