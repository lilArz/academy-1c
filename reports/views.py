from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from warehouse.models import StockRegister
from documents.models import SaleDocument, IncomeDocument
from accounting.models import Payment


@login_required
def report_stock(request):
    stock = StockRegister.objects.select_related('product', 'warehouse').order_by('warehouse')
    return render(request, 'reports/stock.html', {'stock': stock})


@login_required
def report_sales(request):
    sales = SaleDocument.objects.filter(status='posted').select_related('partner', 'warehouse').order_by('-date')
    return render(request, 'reports/sales.html', {'sales': sales})


@login_required
def report_debts(request):
    from documents.models import Invoice
    unpaid = Invoice.objects.filter(status__in=['unpaid', 'partial']).select_related('partner')
    return render(request, 'reports/debts.html', {'unpaid': unpaid})