from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import IncomeDocument, IncomeItem, SaleDocument, SaleItem, Invoice
from .forms import IncomeDocumentForm, IncomeItemForm, SaleDocumentForm, SaleItemForm, InvoiceForm
from warehouse.models import StockRegister, StockMovement


def update_stock(product, warehouse, quantity, movement_type, doc_type, doc_id, date):
    """Обновляем остатки на складе"""
    stock, created = StockRegister.objects.get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={'quantity': 0}
    )
    if movement_type == 'in':
        stock.quantity += quantity
    else:
        stock.quantity -= quantity
    stock.save()

    StockMovement.objects.create(
        product=product,
        warehouse=warehouse,
        movement_type=movement_type,
        quantity=quantity,
        document_type=doc_type,
        document_id=doc_id,
        date=date,
    )


# ========== ПОСТУПЛЕНИЯ ==========
@login_required
def income_list(request):
    docs = IncomeDocument.objects.select_related('partner', 'warehouse').order_by('-date')
    return render(request, 'documents/income_list.html', {'docs': docs})


@login_required
def income_create(request):
    IncomeItemFormSet = inlineformset_factory(
        IncomeDocument, IncomeItem,
        form=IncomeItemForm,
        extra=3, can_delete=True
    )
    if request.method == 'POST':
        form = IncomeDocumentForm(request.POST)
        formset = IncomeItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            formset.instance = doc
            formset.save()
            if doc.status == 'posted':
                for item in doc.items.all():
                    update_stock(item.product, doc.warehouse, item.quantity, 'in', 'Поступление', doc.id, doc.date)
            messages.success(request, f'Поступление №{doc.number} создано!')
            return redirect('documents:income_list')
    else:
        form = IncomeDocumentForm()
        formset = IncomeItemFormSet()
    return render(request, 'documents/income_form.html', {
        'form': form, 'formset': formset, 'title': 'Новое поступление'
    })


@login_required
def income_detail(request, pk):
    doc = get_object_or_404(IncomeDocument, pk=pk)
    items = doc.items.select_related('product')
    return render(request, 'documents/income_detail.html', {'doc': doc, 'items': items})


@login_required
def income_edit(request, pk):
    doc = get_object_or_404(IncomeDocument, pk=pk)
    IncomeItemFormSet = inlineformset_factory(
        IncomeDocument, IncomeItem,
        form=IncomeItemForm,
        extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = IncomeDocumentForm(request.POST, instance=doc)
        formset = IncomeItemFormSet(request.POST, instance=doc)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Поступление обновлено!')
            return redirect('documents:income_list')
    else:
        form = IncomeDocumentForm(instance=doc)
        formset = IncomeItemFormSet(instance=doc)
    return render(request, 'documents/income_form.html', {
        'form': form, 'formset': formset, 'title': 'Редактировать поступление'
    })


@login_required
def income_delete(request, pk):
    doc = get_object_or_404(IncomeDocument, pk=pk)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, 'Поступление удалено!')
        return redirect('documents:income_list')
    return render(request, 'documents/confirm_delete.html', {'object': doc, 'back_url': 'documents:income_list'})


@login_required
def income_post(request, pk):
    """Провести документ — обновить склад"""
    doc = get_object_or_404(IncomeDocument, pk=pk)
    if doc.status != 'posted':
        doc.status = 'posted'
        doc.save()
        for item in doc.items.all():
            update_stock(item.product, doc.warehouse, item.quantity, 'in', 'Поступление', doc.id, doc.date)
        messages.success(request, f'Документ №{doc.number} проведён! Склад обновлён.')
    else:
        messages.warning(request, 'Документ уже проведён.')
    return redirect('documents:income_detail', pk=pk)


# ========== РЕАЛИЗАЦИИ ==========
@login_required
def sale_list(request):
    docs = SaleDocument.objects.select_related('partner', 'warehouse').order_by('-date')
    return render(request, 'documents/sale_list.html', {'docs': docs})


@login_required
def sale_create(request):
    SaleItemFormSet = inlineformset_factory(
        SaleDocument, SaleItem,
        form=SaleItemForm,
        extra=3, can_delete=True
    )
    if request.method == 'POST':
        form = SaleDocumentForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            doc = form.save(commit=False)
            doc.created_by = request.user
            doc.save()
            formset.instance = doc
            formset.save()
            if doc.status == 'posted':
                for item in doc.items.all():
                    update_stock(item.product, doc.warehouse, item.quantity, 'out', 'Реализация', doc.id, doc.date)
            messages.success(request, f'Реализация №{doc.number} создана!')
            return redirect('documents:sale_list')
    else:
        form = SaleDocumentForm()
        formset = SaleItemFormSet()
    return render(request, 'documents/sale_form.html', {
        'form': form, 'formset': formset, 'title': 'Новая реализация'
    })


@login_required
def sale_detail(request, pk):
    doc = get_object_or_404(SaleDocument, pk=pk)
    items = doc.items.select_related('product')
    return render(request, 'documents/sale_detail.html', {'doc': doc, 'items': items})


@login_required
def sale_edit(request, pk):
    doc = get_object_or_404(SaleDocument, pk=pk)
    SaleItemFormSet = inlineformset_factory(
        SaleDocument, SaleItem,
        form=SaleItemForm,
        extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = SaleDocumentForm(request.POST, instance=doc)
        formset = SaleItemFormSet(request.POST, instance=doc)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Реализация обновлена!')
            return redirect('documents:sale_list')
    else:
        form = SaleDocumentForm(instance=doc)
        formset = SaleItemFormSet(instance=doc)
    return render(request, 'documents/sale_form.html', {
        'form': form, 'formset': formset, 'title': 'Редактировать реализацию'
    })


@login_required
def sale_delete(request, pk):
    doc = get_object_or_404(SaleDocument, pk=pk)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, 'Реализация удалена!')
        return redirect('documents:sale_list')
    return render(request, 'documents/confirm_delete.html', {'object': doc, 'back_url': 'documents:sale_list'})


@login_required
def sale_post(request, pk):
    """Провести реализацию — списать со склада"""
    doc = get_object_or_404(SaleDocument, pk=pk)
    if doc.status != 'posted':
        doc.status = 'posted'
        doc.save()
        for item in doc.items.all():
            update_stock(item.product, doc.warehouse, item.quantity, 'out', 'Реализация', doc.id, doc.date)
        messages.success(request, f'Реализация №{doc.number} проведена! Склад обновлён.')
    else:
        messages.warning(request, 'Документ уже проведён.')
    return redirect('documents:sale_detail', pk=pk)


# ========== СЧЕТА ==========
@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('partner').order_by('-date')
    return render(request, 'documents/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_create(request):
    form = InvoiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Счёт создан!')
        return redirect('documents:invoice_list')
    return render(request, 'documents/invoice_form.html', {'form': form, 'title': 'Новый счёт'})


@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        messages.success(request, 'Счёт обновлён!')
        return redirect('documents:invoice_list')
    return render(request, 'documents/invoice_form.html', {'form': form, 'title': 'Редактировать счёт'})


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Счёт удалён!')
        return redirect('documents:invoice_list')
    return render(request, 'documents/confirm_delete.html', {'object': invoice, 'back_url': 'documents:invoice_list'})