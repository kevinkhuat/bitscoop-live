def update(obj, kwargs):
    for key, value in kwargs.items():
        setattr(obj, key, value)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for is not None:
        return x_forwarded_for.split(',')[0].strip()
    else:
        return request.META.get('REMOTE_ADDR')
