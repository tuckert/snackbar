"""DriveInMenu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import home_page
from django.conf.urls.static import static
from django.conf import settings
from snackbar.views import menu_view, add_item_to_order, remove_item_from_order
from orders.views import checkout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('menu/', menu_view, name='menu'),
    path('add_item/<pk>/', add_item_to_order, name='add-item-to-order'),
    path('remove_item/<pk>', remove_item_from_order, name='remove-item-from-order'),
    path('stripe/', include('djstripe.urls', namespace='djstripe')),
    path('checkout/', checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
