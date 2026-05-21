from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('stock/', views.report_stock, name='stock'),
    path('sales/', views.report_sales, name='sales'),
    path('debts/', views.report_debts, name='debts'),
]