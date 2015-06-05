from collections import Iterable

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.utils.module_loading import import_string


def extract_patterns(inst, path='', patterns=[]):
    if isinstance(inst, Iterable):
        if isinstance(inst, str):
            inst = import_string('{0}.{1}'.format(inst, 'urlpatterns'))

        for component in inst:
            extract_patterns(component, path, patterns)

        return patterns

    path = (path + ' ' + inst.regex.pattern).strip()

    if isinstance(inst, RegexURLPattern):
        patterns.append(path)
    elif isinstance(inst, RegexURLResolver):
        extract_patterns(inst.url_patterns, path, patterns)

    return patterns


class Command(BaseCommand):
    help = 'Displays all of the url matching routes for the project.'

    def handle(self, *args, **options):
        patterns = extract_patterns(settings.ROOT_URLCONF)

        return '\n'.join(patterns)
