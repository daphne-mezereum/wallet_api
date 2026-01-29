from django.test import TestCase
from decimal import Decimal
import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Wallet


class WalletDetailViewTests(APITestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create(balance=Decimal("123.45"))
        self.url = reverse("wallet_detail", kwargs={"uuid": self.wallet.uuid})

    def test_get_wallet_balance_success(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["uuid"], str(self.wallet.uuid))
        self.assertEqual(resp.data["balance"], "123.45")

    def test_get_wallet_balance_not_found(self):
        missing_uuid = uuid.uuid4()
        url = reverse("wallet_detail", kwargs={"uuid": missing_uuid})

        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
