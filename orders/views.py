from django.shortcuts import render
from .forms import OrderItemForm
from django.forms import formset_factory, modelformset_factory
from .models import Order, OrderItem


# Create your views here.
def checkout(request):
    order, created = Order.objects.get_or_create(user=request.user, order_placed_at=None,
                                                 defaults={
                                                     'user': request.user,
                                                 })
    OrderItemFormSet = modelformset_factory(OrderItem, extra=0, form=OrderItemForm)
    print(order.items.filter(quantity__gt=0))
    formset = OrderItemFormSet(queryset=order.items.filter(quantity__gt=0))
    print(formset)
    context = {
        'formset': formset,
        'order': order,
    }
    return render(request, 'checkout.html', context)
