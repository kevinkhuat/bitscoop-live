import urllib2


def get_url_content(request_url):
    request = urllib2.Request(request_url)
    response = urllib2.urlopen(request)

    return response.read()