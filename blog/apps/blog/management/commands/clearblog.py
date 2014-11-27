from django.core.management.base import BaseCommand

from ografy.apps.blog.models import Article, Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Article.objects.all().delete()
        Tag.objects.all().delete()

        # TODO: Remove formatted blog templates from `/templates/blog/posts`.
