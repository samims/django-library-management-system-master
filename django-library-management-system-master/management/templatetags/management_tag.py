from django import template
from library.models import Borrow, Student

register = template.Library()


@register.filter
def filter_borrow(value):
    borrowed_list = Borrow.objects.filter(status=value)
    return borrowed_list
