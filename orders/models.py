from django.db import models
from django.contrib.auth.models import User
import json
from django.db.models.signals import pre_save, post_init, post_save, pre_init
from datetime import datetime
from items.models import Item
from django.db.models import Q
from django.contrib import messages


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_placed_at = models.DateTimeField(null=True, blank=True)
    out_for_delivery_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    total = models.FloatField(default=0)

    def __str__(self):
        if self.active:
            return self.user.username + "'s order"
        else:
            return self.user.username + "'s order (PLACED)"

    # Return true if Order hasn't been placed yet
    @property
    def active(self):
        if self.order_placed_at:
            return False
        else:
            return True


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='sales')
    quantity = models.IntegerField(default=0)
    special_instructions = models.TextField(blank=True, default=None, null=True)
    name = models.CharField(max_length=80)
    price = models.FloatField()

    # Returns a total based on quantity and price
    @property
    def total(self):
        return float(self.quantity) * self.price

    def __str__(self):
        return self.order.__str__() + ' ' + self.name


# Check quantity against availability
# also checks price
def pre_save_order_item_sync(sender, instance, *args, **kwargs):
    # Make sure order is active before we change details about it
    if not instance.order.active:
        return

    # Make sure we have enough items in inventory.
    if instance.quantity > instance.item.quantity and not instance.item.unlimited:
        instance.quantity = instance.item.quantity

    # Check the price against the item every save and adjust accordingly
    if instance.item is not None and instance.price != instance.item.price:
        instance.price = instance.item.price

# Connect it to the OrderItem post_save signal
pre_save.connect(pre_save_order_item_sync, sender=OrderItem)


# Post save order total calculator
def post_save_order_total(sender, instance, *args, **kwargs):
    # Add the totals for each item in the order
    items = instance.order.items.all()
    instance.order.total = sum([item.total for item in items])
    instance.order.save()


post_save.connect(post_save_order_total, sender=OrderItem)


# Checks for new items in the database every time an Order is pulled.
# Must be post_save to create a list of new Order Items
def post_save_order_item_sync(sender, instance, *args, **kwargs):

    # If the order has already been place, delete unused items and return.
    if not instance.active:
        instance.items.filter(quantity=0).delete()
        # TODO Make sure an order is available for the user to begin a cart.
        return
    available_items = Item.objects.filter(Q(unlimited=True, active=True) | Q(quantity__gt=0, active=True))

    new_items_for_sale = available_items.exclude(sales__in=instance.items.all())

    # Create new Order Items for the order
    if new_items_for_sale:

        # List of OrderItem objects to be bulk_created
        order_list = []
        for item in new_items_for_sale:
            order_item = OrderItem(
                order=instance,
                item=item,
                quantity=0,
                name=item.name,
                price=item.price,
            )
            order_list.append(order_item)
        # Create
        OrderItem.objects.bulk_create(order_list)

    # Remove items that have been disabled from the order items list
    instance.items.all().exclude(item__in=available_items).delete()


# Connect it to the Signal
post_save.connect(post_save_order_item_sync, sender=Order)






