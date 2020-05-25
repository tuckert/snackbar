from django.db.models.signals import pre_save
from django.dispatch import receiver
from orders.models import Order
import json


def items_to_json(sender, **kwargs):
    sender.items_json = json.dumps(sender.items)
    print('pre_save ran')


pre_save.connect(items_to_json)
