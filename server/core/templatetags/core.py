from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def relative_time(value):
    now = timezone.now()

    delta = now - value
    seconds = delta.total_seconds()
    abs_seconds = abs(seconds)

    if abs_seconds < 45:  # 45 sec
        text = 'a few seconds'
    elif abs_seconds < 90:  # 90 sec
        text = 'a minute'
    elif abs_seconds < 2700:  # 45 min
        text = '{0} minutes'.format(int(abs_seconds / 60))
    elif abs_seconds < 5400:  # 90 min
        text = 'an hour'
    elif abs_seconds < 79200:  # 22 hours
        text = '{0} hours'.format(int(abs_seconds / (60 * 60)))
    elif abs_seconds < 129600:  # 36 hours
        text = 'a day'
    elif abs_seconds < 2160000:  # 25 days
        text = '{0} days'.format(int(abs_seconds / (60 * 60 * 24)))
    elif abs_seconds < 3888000:  # 45 days
        text = 'a month'
    elif abs_seconds < 29808000:  # 345 days
        text = '{0} months'.format(int(abs_seconds / (60 * 60 * 24 * 30)))
    elif abs_seconds < 47088000:  # 545 days
        text = 'a year'
    else:
        text = '{0} years'.format(int(abs_seconds / (60 * 60 * 24 * 365)))

    if seconds < 0:
        text = 'in {0}'.format(text)
    else:
        text = '{0} ago'.format(text)

    return text
