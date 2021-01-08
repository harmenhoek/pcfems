from django import template
from datetime import date
import math
import os
from django.conf import settings

register = template.Library()

@register.filter
def in_the_future(value):
    if value is None:
        return False
    else:
        return value > date.today()

@register.filter()
def timedelta(value):
    curr_date = date.today()
    diff = value - curr_date
    year = diff.days // (365.25)
    month = (diff.days - year * 365.25) // (365.25 / 12)
    day = ((diff.days - year * 365.25) - month * (365.25 / 12))
    dt = ''
    if (year < 0):
        dt = 'overdue'
    else:
        if (year != 0):
            dt = dt + str(int(year)) + ' years'
            if (month != 0 or day != 0):
                dt = dt + ', '
        if (month != 0):
            dt = dt + str(int(month)) + ' months'
            if (day != 0):
                dt = dt + ', '
        if (day != 0):
            dt = dt + str(int(math.ceil(day))) + ' days'
        if (year == 0 and month == 0 and day == 0):
            dt = 'today'
    return dt

@register.filter
def filesize(value):
    """Returns the filesize of the filename given in value"""
    return os.path.getsize(value)

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")