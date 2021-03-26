from django import template
from core.models import Order

register = template.Library()

@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user= user, ordered=False)
        total = 0
        if qs.exists():
            for product in qs[0].products.all():
                total += product.quantity
        return total
    return 0

