from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('payments/', views.payment_list, name='payment_list'),
]