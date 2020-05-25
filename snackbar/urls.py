from django.urls import path, include
from .views import menu_view

app_name = "snackbar"
urlpatterns = [
    path('<slug>/menu', menu_view, name='menu')
]
