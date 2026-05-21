from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment


@login_required
def payment_list(request):
    payments = Payment.objects.select_related('partner', 'invoice').order_by('-date')
    return render(request, 'accounting/payment_list.html', {'payments': payments})