from django import template
import locale
import decimal
register =  template.Library()

@register.filter(name="add_class")
def add_class(value):
    return value.replace('-','')


locale.setlocale(locale.LC_MONETARY, 'en_IN') 
@register.filter()
def currency(value):
    value = decimal.Decimal(value)
    return locale.currency(value, grouping=True)