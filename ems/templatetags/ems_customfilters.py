from django import template
from datetime import date
import math
import os
from django.conf import settings
from datetime import datetime

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

@register.filter
def nonevalue(value):
    if value:
        return value
    else:
        return f"<em class='text-muted'>{value}</em>"

@register.filter
def unknown(value):
    if value:
        return value
    else:
        return f"<em class='text-muted'>Unknown</em>"


@register.filter
def defaultifempty(value):
    if value:
        return value.url
    else:
        return f"{settings.MEDIA_URL}{settings.DEFAULT_IMAGE}"

# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

@register.filter()
def check_permission(user, permission):
    if user.user_permissions.filter(codename = permission).exists():
        return True
    return False


from django.contrib.contenttypes.models import ContentType
from users.models import Profile

@register.filter()
def get_all_permissions(user):
    content_type = ContentType.objects.get_for_model(Profile)
    perms = user.user_permissions.filter(content_type=content_type)
    perms_codename = [perm.codename for perm in perms]
    perms_name = [perm.name for perm in perms]

    if not perms:
        return ""
    else:
        return zip(perms_codename, perms_name)

@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)

@register.filter(expects_localtime=True)
def weeks_since(value, arg=None):
    try:
        tzinfo = getattr(value, 'tzinfo', None)
        value = date(value.year, value.month, value.day)
    except AttributeError:
        # Passed value wasn't a date object
        return value
    except ValueError:
        # Date arguments out of range
        return value
    today = datetime.now(tzinfo).date()
    delta = value - today
    if abs(delta.days * 7) == 1:
        day_str = " week"
    else:
        day_str = " weeks"

    if delta.days * 7 < 1:
        fa_str =" ago"
    else:
        fa_str = " from now"

    return str(round(abs(delta.days / 7))) + day_str + fa_str