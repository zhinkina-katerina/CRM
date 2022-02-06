from django import template

register = template.Library()

from ..models import Delivery

@register.filter
def human_readable_delivery(value, arg):
    for choise in Delivery.STATUS_CHOICES:
        if arg in choise:
            return choise[1]
