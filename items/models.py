from django.db import models
import json
from django.db.models.signals import pre_save


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='items')
    unlimited = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    max_per_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    modified_at = models.DateTimeField(null=True)
    picture = models.ImageField(upload_to='items', default=None, null=True)

    def __str__(self):
        return self.name


# On item edit, trigger save function for all corresponding Order items to update cart prices