def page_name(request):
    resolver_match = request.resolver_match

    name = resolver_match.url_name

    if resolver_match.namespace:
        namespace = resolver_match.namespace.replace(':', ' ')
        name = namespace + ' ' + name

    if resolver_match.app_name:
        name = resolver_match.app_name + ' ' + name

    if request.user.is_authenticated():
        name = 'authenticated ' + name

    return {
        'page_name': name
    }
