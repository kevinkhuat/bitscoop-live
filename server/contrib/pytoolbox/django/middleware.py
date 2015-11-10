class AcceptMiddleware(object):
    def _parse(self, accept):
        result = []

        for media_range in accept.split(','):
            parts = media_range.split(';')
            media_type = parts.pop(0).lstrip()
            media_params = []
            q = 1.0

            for part in parts:
                key, value = part.lstrip().split('=', 1)

                if key == 'q':
                    try:
                        q = float(value)
                    except ValueError:
                        pass
                else:
                    media_params.append((key, value))

            result.append((media_type, tuple(media_params), q))

        result.sort(key=lambda t: t[2], reverse=True)

        return result

    def process_request(self, request):
        accept = request.META.get('HTTP_ACCEPT')

        if accept:
            parsed = self._parse(accept)
            request.accepted_types = list(map(lambda t: t[0], parsed))
        else:
            request.accepted_types = ['*/*']


class SetAnonymousTestCookie(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            request.session.set_test_cookie()

        return None
