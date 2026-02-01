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


class WalletOperationsTest(APITestCase):
    default_balance = Decimal('500.50')

    def setUp(self):
        self.wallet = Wallet.objects.create(balance=self.default_balance)
        self.url = reverse("wallet_operation", kwargs={"uuid": self.wallet.uuid})

    def test_deposit_increases_balance(self):
        payload = {"operation_type": "DEPOSIT", "amount": "50.00"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("550.50"))

    def test_withdraw_decreases_balance(self):
        payload = {"operation_type": "WITHDRAW", "amount": "20.00"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("480.50"))

    def test_withdraw_insufficient_funds(self):
        payload = {"operation_type": "WITHDRAW", "amount": "999.00"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, self.default_balance)

    def test_wallet_not_found(self):
        missing_uuid = uuid.uuid4()
        url = reverse("wallet_operation", kwargs={"uuid": missing_uuid})

        payload = {"operation_type": "DEPOSIT", "amount": "10.00"}
        resp = self.client.post(url, payload, format="json")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_operation_type(self):
        payload = {"operation_type": "RANDOM", "amount": "10.00"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, self.default_balance)

    def test_invalid_amount(self):
        payload = {"operation_type": "DEPOSIT", "amount": "0.00"}  # min_value=0.01

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, self.default_balance)

    def test_invalid_accuracy(self):
        payload = {"operation_type": "DEPOSIT", "amount": "5.5625"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, self.default_balance)

    def test_invalid_max_digits(self):
        payload = {"operation_type": "DEPOSIT", "amount": "6548549769674967496549535494544653"}

        resp = self.client.post(self.url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, self.default_balance)
