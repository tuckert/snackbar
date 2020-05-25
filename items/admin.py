from django.contrib import admin
from items.models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
