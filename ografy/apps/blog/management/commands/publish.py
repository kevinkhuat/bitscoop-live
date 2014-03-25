from __future__ import unicode_literals
from datetime import datetime
import os
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ografy.apps.blog.models import Article, Tag

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        root_dir = os.getcwd()
        read_dir = os.path.abspath(os.path.join(root_dir, 'blog'))
        pub_dir = os.path.abspath(os.path.join(root_dir, 'ografy', 'templates', 'blog', 'posts'))

        if not os.path.exists(pub_dir):
            os.makedirs(pub_dir)

        files = []
        for (dirpath, dirnames, filenames) in os.walk(read_dir):
            files.extend(filenames)
            break

        for filename in files:
            read_file = os.path.join(read_dir, filename)
            name, ext = os.path.splitext(filename)

            buffer = ''
            properties = {
                'title': name,
                'date': None,
                'tags': []
            }

            with open(read_file, 'r') as infile:
                for line in infile:
                    match_obj = re.match(r'^@(\w+) (.+)$', line)

                    if match_obj:
                        key = match_obj.group(1)
                        value = match_obj.group(2)

                        if key == 'title':
                            properties[key] = value
                        elif key == 'author':
                            properties[key] = value
                        elif key == 'date':
                            properties[key] = datetime.strptime(value, '%m/%d/%Y')
                        elif key == 'tags':
                            properties[key] = re.split(r',\s*', value)
                    else:
                        buffer += line

            timestamp = int(os.path.getmtime(read_file))
            modified = datetime.fromtimestamp(timestamp)
            slug = slugify(name)

            self.stdout.write('\n{0} => {1}'.format(slug, modified))
            self.stdout.write('Tags: {0}'.format(properties['tags']))

            if 'author' in properties:
                author = User.objects.by_identifier(properties['author']).first()
            else:
                author = None

            if author is not None:
                self.stdout.write('Author: {0}'.format(author.identifier))
            else:
                self.stdout.write('No author found.')

            article = Article.objects.filter(slug__exact=slug).first()
            if article is not None:
                article.title = properties['title']
                article.slug = slug
                article.posted = properties['date']
                article.updated = modified
                article.author = author
            else:
                self.stdout.write('Publishing `{0}` to db.'.format(slug))
                article = Article(
                    title=properties['title'],
                    slug=slug,
                    posted=properties['date'],
                    updated=modified
                )
                article.author = author
                article.save()

            for tag_name in properties['tags']:
                tag = Tag.objects.filter(name__exact=tag_name).first()
                tag_slug = slugify(tag_name)

                if tag is None:
                    self.stdout.write('Creating tag `{0}` in db.'.format(tag_slug))
                    tag = Tag(name=tag_name)
                    tag.save()

                if not article.tags.filter(slug=tag_slug).exists():
                    tag.articles.add(article)

            write_file = os.path.join(pub_dir, '{0}{1}'.format(slug, ext))
            with open(write_file, 'w') as outfile:
                outfile.write('{% extends \'blog/article.html\' %}\n\n')
                outfile.write('{% block article %}\n')
                outfile.write(buffer.strip())
                outfile.write('\n{% endblock %}')
