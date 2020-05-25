from django.shortcuts import render
from orders.models import Order
from items.models import Item, Category


# Create your views here.
def home_page(request, ):
    items = Category.objects.all()

    return render(request, 'home.html', context={'items': items})
