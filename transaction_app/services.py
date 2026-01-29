from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import APIException
from .models import Wallet
from .exceptions import Conflict


def apply_wallet_operation(*, wallet_uuid, operation_type, amount) -> Wallet:

    with transaction.atomic():
        wallet = get_object_or_404(Wallet.objects.select_for_update(), uuid=wallet_uuid)

        if operation_type == "DEPOSIT":
            wallet.balance += amount

        elif operation_type == "WITHDRAW":
            if wallet.balance < amount:
                raise Conflict("Insufficient funds")
            wallet.balance -= amount

        else:
            raise APIException("Invalid operation type")

        wallet.save(update_fields=["balance", 'updated_at'])

    return wallet
