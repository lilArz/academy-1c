from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('stock/', views.stock_list, name='stock_list'),
    path('movements/', views.movement_list, name='movement_list'),
]