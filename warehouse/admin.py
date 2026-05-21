from django.contrib import admin
from .models import StockRegister, StockMovement


@admin.register(StockRegister)
class StockRegisterAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    list_filter = ('warehouse',)
    search_fields = ('product__name',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'movement_type', 'product', 'warehouse', 'quantity', 'document_type', 'document_id')
    list_filter = ('movement_type', 'warehouse', 'date')
    search_fields = ('product__name',)
    readonly_fields = ('created_at',)