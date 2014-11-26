from django.utils.text import slugify as base_slugify


def slugify(value):
    unic = str(value)

    return base_slugify(unic)
