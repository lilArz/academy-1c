from django import forms
from .models import IncomeDocument, IncomeItem, SaleDocument, SaleItem, Invoice
from references.models import Product, Partner, Warehouse


class IncomeDocumentForm(forms.ModelForm):
    class Meta:
        model = IncomeDocument
        fields = ['number', 'date', 'partner', 'warehouse', 'status', 'comment']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер документа'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'partner': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class IncomeItemForm(forms.ModelForm):
    class Meta:
        model = IncomeItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }


class SaleDocumentForm(forms.ModelForm):
    class Meta:
        model = SaleDocument
        fields = ['number', 'date', 'partner', 'warehouse', 'status', 'comment']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер документа'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'partner': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'date', 'partner', 'sale', 'amount', 'status', 'due_date']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'partner': forms.Select(attrs={'class': 'form-select'}),
            'sale': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }