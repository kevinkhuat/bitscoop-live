from django.conf import settings
from django.db import models

from ografy.util.decorators import autoconnect
from ografy.util.encoding import slugify


@autoconnect
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, blank=False, unique=True)
    slug = models.CharField(max_length=120, blank=False, unique=True, db_index=True)
    posted = models.DateTimeField()
    updated = models.DateTimeField()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    def pre_save(self):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)


@autoconnect
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True, db_index=True)

    articles = models.ManyToManyField(Article, related_name='tags')

    def pre_save(self):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)
