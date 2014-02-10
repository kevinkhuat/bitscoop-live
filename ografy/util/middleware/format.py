from django.conf import settings


class RenderFormat(object):
    """
    Modifies the request with flags indicating
        - xhr: XMLHttpRequest request access specified by X-Requested-With
        - mobile: Mobile request
    """

    def process_request(self, request):
        request.xhr = request.is_ajax()

        user_agent = request.META['HTTP_USER_AGENT']
        browser = settings.MOBILE_REGEXP['BROWSER'].search(user_agent)
        version = settings.MOBILE_REGEXP['VERSION'].search(user_agent[0:4])
        request.mobile = browser or version

        return None