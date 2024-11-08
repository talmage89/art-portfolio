from django import template

register = template.Library()


@register.filter
def cents_to_dollars(cents):
    if not isinstance(cents, (int, float)):
        try:
            cents = int(cents)
        except (ValueError, TypeError):
            return "0.00"
    if cents is None:
        return "0.00"
    return "{:.2f}".format(cents / 100)


@register.filter
def get_item(dictionary, key):
    print(dictionary, key)
    return dictionary.get(key)
