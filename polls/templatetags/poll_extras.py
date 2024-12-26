from django import template
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='cut')
def cut(value, arg):
    return value.replace(arg, '')


@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)


@register.filter(name='show_jalali_time')
def show_jalali_time(value):
    return value.strftime('%H:%M')


@register.filter(name='three_degit_currency')
def three_digit_currency(value: int):
    return '{:,}'.format(value) + ' تومان'


@register.simple_tag
def multiply(quantity, price, *args, **kwargs):
    return three_digit_currency(quantity * price)
