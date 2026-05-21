from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Partner, Warehouse
from .forms import ProductForm, PartnerForm, WarehouseForm


@login_required
def dashboard(request):
    from documents.models import SaleDocument, IncomeDocument
    from warehouse.models import StockRegister
    total_products = Product.objects.filter(is_active=True).count()
    total_partners = Partner.objects.filter(is_active=True).count()
    total_sales = SaleDocument.objects.filter(status='posted').count()
    total_income = IncomeDocument.objects.filter(status='posted').count()
    low_stock = StockRegister.objects.filter(quantity__lte=5)
    context = {
        'total_products': total_products,
        'total_partners': total_partners,
        'total_sales': total_sales,
        'total_income': total_income,
        'low_stock': low_stock,
    }
    return render(request, 'dashboard.html', context)


# ========== ТОВАРЫ ==========
@login_required
def product_list(request):
    products = Product.objects.select_related('category', 'unit').all()
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'references/product_list.html', {'products': products, 'query': query})


@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Товар успешно добавлен!')
        return redirect('references:product_list')
    return render(request, 'references/product_form.html', {'form': form, 'title': 'Новый товар'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        messages.success(request, 'Товар обновлён!')
        return redirect('references:product_list')
    return render(request, 'references/product_form.html', {'form': form, 'title': 'Редактировать товар'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удалён!')
        return redirect('references:product_list')
    return render(request, 'references/confirm_delete.html', {'object': product, 'title': 'товар'})


# ========== КОНТРАГЕНТЫ ==========
@login_required
def partner_list(request):
    partners = Partner.objects.all()
    query = request.GET.get('q')
    if query:
        partners = partners.filter(name__icontains=query)
    return render(request, 'references/partner_list.html', {'partners': partners, 'query': query})


@login_required
def partner_create(request):
    form = PartnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Контрагент добавлен!')
        return redirect('references:partner_list')
    return render(request, 'references/partner_form.html', {'form': form, 'title': 'Новый контрагент'})


@login_required
def partner_edit(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    form = PartnerForm(request.POST or None, instance=partner)
    if form.is_valid():
        form.save()
        messages.success(request, 'Контрагент обновлён!')
        return redirect('references:partner_list')
    return render(request, 'references/partner_form.html', {'form': form, 'title': 'Редактировать контрагента'})


@login_required
def partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    if request.method == 'POST':
        partner.delete()
        messages.success(request, 'Контрагент удалён!')
        return redirect('references:partner_list')
    return render(request, 'references/confirm_delete.html', {'object': partner, 'title': 'контрагента'})


# ========== СКЛАДЫ ==========
@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'references/warehouse_list.html', {'warehouses': warehouses})


@login_required
def warehouse_create(request):
    form = WarehouseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Склад добавлен!')
        return redirect('references:warehouse_list')
    return render(request, 'references/warehouse_form.html', {'form': form, 'title': 'Новый склад'})


@login_required
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    form = WarehouseForm(request.POST or None, instance=warehouse)
    if form.is_valid():
        form.save()
        messages.success(request, 'Склад обновлён!')
        return redirect('references:warehouse_list')
    return render(request, 'references/warehouse_form.html', {'form': form, 'title': 'Редактировать склад'})


@login_required
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.delete()
        messages.success(request, 'Склад удалён!')
        return redirect('references:warehouse_list')
    return render(request, 'references/confirm_delete.html', {'object': warehouse, 'title': 'склад'})