from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StockRegister, StockMovement


@login_required
def stock_list(request):
    stock = StockRegister.objects.select_related('product', 'warehouse').order_by('warehouse', 'product')
    query = request.GET.get('q')
    if query:
        stock = stock.filter(product__name__icontains=query)
    return render(request, 'warehouse/stock_list.html', {'stock': stock, 'query': query})


@login_required
def movement_list(request):
    movements = StockMovement.objects.select_related('product', 'warehouse').order_by('-date')
    return render(request, 'warehouse/movement_list.html', {'movements': movements})