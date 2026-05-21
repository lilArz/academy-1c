from django.db import models
from django.contrib.auth.models import User
from references.models import Product, Partner, Warehouse


class IncomeDocument(models.Model):
    """Поступление товаров"""
    STATUS = [
        ('draft', 'Черновик'),
        ('posted', 'Проведён'),
        ('cancelled', 'Отменён'),
    ]
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Поставщик')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name='Склад')
    status = models.CharField(max_length=20, choices=STATUS, default='draft', verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Поступление'
        verbose_name_plural = 'Поступления'

    def __str__(self):
        return f'Поступление №{self.number} от {self.date}'

    def get_total(self):
        return sum(item.get_amount() for item in self.items.all())


class IncomeItem(models.Model):
    """Строка поступления"""
    document = models.ForeignKey(IncomeDocument, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Количество')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Строка поступления'
        verbose_name_plural = 'Строки поступления'

    def get_amount(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.product} x {self.quantity}'


class SaleDocument(models.Model):
    """Реализация товаров"""
    STATUS = [
        ('draft', 'Черновик'),
        ('posted', 'Проведён'),
        ('cancelled', 'Отменён'),
    ]
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Покупатель')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name='Склад')
    status = models.CharField(max_length=20, choices=STATUS, default='draft', verbose_name='Статус')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Реализация'
        verbose_name_plural = 'Реализации'

    def __str__(self):
        return f'Реализация №{self.number} от {self.date}'

    def get_total(self):
        return sum(item.get_amount() for item in self.items.all())


class SaleItem(models.Model):
    """Строка реализации"""
    document = models.ForeignKey(SaleDocument, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.DecimalField(max_digits=12, decimal_places=3, verbose_name='Количество')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Строка реализации'
        verbose_name_plural = 'Строки реализации'

    def get_amount(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.product} x {self.quantity}'


class Invoice(models.Model):
    """Счёт на оплату"""
    STATUS = [
        ('unpaid', 'Не оплачен'),
        ('paid', 'Оплачен'),
        ('partial', 'Частично оплачен'),
    ]
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Контрагент')
    sale = models.ForeignKey(SaleDocument, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Реализация')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=STATUS, default='unpaid', verbose_name='Статус')
    due_date = models.DateField(null=True, blank=True, verbose_name='Срок оплаты')

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'

    def __str__(self):
        return f'Счёт №{self.number} от {self.date}'