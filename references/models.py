from django.db import models


class Unit(models.Model):
    """Единица измерения"""
    name = models.CharField(max_length=50, verbose_name='Название')
    short_name = models.CharField(max_length=10, verbose_name='Краткое')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.short_name


class Category(models.Model):
    """Категория товара"""
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Номенклатура / Товар"""
    code = models.CharField(max_length=20, unique=True, verbose_name='Код')
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Ед. изм.')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.code} — {self.name}'


class Partner(models.Model):
    """Контрагент"""
    PARTNER_TYPE = [
        ('supplier', 'Поставщик'),
        ('buyer', 'Покупатель'),
        ('both', 'Поставщик и покупатель'),
    ]
    name = models.CharField(max_length=200, verbose_name='Название')
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPE, default='buyer', verbose_name='Тип')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')
    inn = models.CharField(max_length=20, blank=True, verbose_name='ИНН')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    """Склад"""
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.TextField(blank=True, verbose_name='Адрес')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name