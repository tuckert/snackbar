from django.shortcuts import render, redirect
from snackbar.models import SnackBar
from items.models import Category
from orders.models import Order, OrderItem
from orders.forms import OrderItemForm
from django.forms import formset_factory, modelformset_factory
from items.models import Item
import datetime
from django.contrib import messages


def menu_view(request):
    order, created = Order.objects.get_or_create(user=request.user, order_placed_at=None,
                                                 defaults={
                                                     'user': request.user,
                                                 })
    OrderItemFormSet = modelformset_factory(OrderItem, extra=0, form=OrderItemForm)
    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST, queryset=order.items.all())
        if formset.is_valid():
            formset.save()
            order.refresh_from_db()
    else:
        formset = OrderItemFormSet(queryset=order.items.all())
    context = {
        'snackbar': SnackBar.objects.first,
        'categories': Category.objects.all,
        'order_formset': formset,
        'order': order,
    }
    return render(request, 'menu.html', context=context)


def add_item_to_order(request, pk):
    order, created = Order.objects.get_or_create(user=request.user, order_placed_at=None)
    item = Item.objects.get(pk=pk)
    order.items['items'].append({
        'name': item.name,
        'price': item.price,
        'quantity': '1',
        'special_instructions': '',
        'item_pk': item.pk
    })
    order.save()

    return redirect('menu')


def remove_item_from_order(request, pk):
    order = Order.objects.get(user=request.user, order_placed_at=None)
    if order:
        item = Item.objects.get(pk=pk)
        new_items = [i for i in order.items['items'] if i.get('item_pk') != item.pk]
        order.items['items'] = new_items
        order.save()
    return redirect('menu')
