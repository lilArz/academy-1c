from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLES = [
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('storekeeper', 'Кладовщик'),
        ('accountant', 'Бухгалтер'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='manager', verbose_name='Роль')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} — {self.get_role_display()}'