from django import forms
from items.models import Item
from django.forms import formset_factory
from .models import OrderItem, Order


bootstrap_form_attrs = {
    'class': 'form-control form-control-lg my-2'
}


class OrderItemForm(forms.ModelForm):

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),
        disabled=True,
        widget=forms.HiddenInput(),
    )

    quantity = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(
            attrs=bootstrap_form_attrs
        )
    )

    special_instructions = forms.CharField(
        label='Special instructions:',
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control my-2'}
        )
    )

    item = forms.ModelChoiceField(
        disabled=True,
        queryset=Item.objects.filter(active=True),
        widget=forms.HiddenInput()
    )

    price = forms.CharField(
        disabled=True,
        widget=forms.HiddenInput()
    )

    name = forms.CharField(
        disabled=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = OrderItem
        fields = '__all__'
