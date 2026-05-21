from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'partner', 'amount', 'payment_type', 'invoice')
    list_filter = ('payment_type', 'date')
    search_fields = ('number', 'partner__name')
    readonly_fields = ('created_at',)