from django.contrib import admin
from .models import Unit, Category, Product, Partner, Warehouse


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('code', 'name')
    list_editable = ('price', 'is_active')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner_type', 'phone', 'email', 'is_active')
    list_filter = ('partner_type', 'is_active')
    search_fields = ('name', 'inn', 'phone')
    list_editable = ('is_active',)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_active')
    list_editable = ('is_active',)