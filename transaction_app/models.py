from django.db import models
import uuid


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
