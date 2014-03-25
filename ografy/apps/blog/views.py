from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render

from ografy.apps.blog.models import Article


def index(request):
    get_all = request.REQUEST.get('all') == '1'

    if get_all:
        articles = Article.objects.all()
    else:
        articles = Article.objects.all()[:5]

    return render(request, 'blog/index.html', {
        'title': 'Ografy - Blog',
        'articles': articles,
        'all': get_all
    })


def post(request, slug):
    article = get_object_or_404(Article, slug=slug)

    return render(request, 'blog/posts/{0}.html'.format(slug), {
        'title': 'Ografy - {0}'.format(article.title),
        'article': article
    })
