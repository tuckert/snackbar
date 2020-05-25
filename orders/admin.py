from django.contrib import admin
from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['total']


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    readonly_fields = ['price']


admin.site.register(OrderItem, OrderItemAdmin)
