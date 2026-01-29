from django.contrib import admin
from .models import Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'balance', 'created_at', 'updated_at')
    list_filter = ['uuid']
    search_fields = ['uuid']
    ordering = ['uuid']

admin.site.register(Wallet, WalletAdmin)
