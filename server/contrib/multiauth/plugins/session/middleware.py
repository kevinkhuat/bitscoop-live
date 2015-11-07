class IpMiddleware(object):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for is not None:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        request.ip = ip


class SessionTrackingMiddleware(object):
    def process_request(self, request):
        # session_key = request.session.session_key
        # is_temporary = request.session.get_expire_at_browser_close()
        # is_anonymous = request.user.is_anonymous()

        return None
