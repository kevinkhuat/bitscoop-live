from __future__ import unicode_literals
import datetime

from django.utils.timezone import now


def offset(seconds=0, minutes=0, hours=0, days=0, weeks=0, delta=None):
    if delta is None:
        delta = datetime.timedelta(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks
        )

    return now() + delta
