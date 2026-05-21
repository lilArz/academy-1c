from django.db import models
from references.models import Product, Warehouse


class StockRegister(models.Model):
    """Остатки товаров на складе"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name='Склад')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0, verbose_name='Остаток')

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f'{self.product} на {self.warehouse}: {self.quantity}'


class StockMovement(models.Model):
    """Движение товаров"""
    MOVEMENT_TYPE = [
        ('in', 'Приход'),
        ('out', 'Расход'),
    ]
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name='Склад')
    movement_type = models.CharField(max_length=5, choices=MOVEMENT_TYPE, verbose_name='Тип')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Количество')
    document_type = models.CharField(max_length=50, verbose_name='Тип документа')
    document_id = models.IntegerField(verbose_name='ID документа')
    date = models.DateField(verbose_name='Дата')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Движение'
        verbose_name_plural = 'Движения'

    def __str__(self):
        return f'{self.get_movement_type_display()} {self.product} — {self.quantity}'