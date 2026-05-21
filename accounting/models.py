from django.db import models
from references.models import Partner
from documents.models import Invoice


class Payment(models.Model):
    """Оплата"""
    PAYMENT_TYPE = [
        ('income', 'Входящая'),
        ('outcome', 'Исходящая'),
    ]
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT, verbose_name='Контрагент')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Счёт')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE, verbose_name='Тип')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'Оплата №{self.number} от {self.date} — {self.amount}'