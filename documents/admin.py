from django.contrib import admin
from .models import IncomeDocument, IncomeItem, SaleDocument, SaleItem, Invoice


class IncomeItemInline(admin.TabularInline):
    model = IncomeItem
    extra = 1
    fields = ('product', 'quantity', 'price')


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ('product', 'quantity', 'price')


@admin.register(IncomeDocument)
class IncomeDocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'partner', 'warehouse', 'status', 'get_total')
    list_filter = ('status', 'date', 'warehouse')
    search_fields = ('number', 'partner__name')
    inlines = [IncomeItemInline]
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_total(self, obj):
        return f'{obj.get_total()} сом'
    get_total.short_description = 'Сумма'


@admin.register(SaleDocument)
class SaleDocumentAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'partner', 'warehouse', 'status', 'get_total')
    list_filter = ('status', 'date', 'warehouse')
    search_fields = ('number', 'partner__name')
    inlines = [SaleItemInline]
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_total(self, obj):
        return f'{obj.get_total()} сом'
    get_total.short_description = 'Сумма'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'partner', 'amount', 'status', 'due_date')
    list_filter = ('status', 'date')
    search_fields = ('number', 'partner__name')
    list_editable = ('status',)