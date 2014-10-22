import urllib2


class Signal(object):
    def __init__(self, url):
        self.url = url

    def scrape(self):
        if self.url is None:
            return None

        request = urllib2.Request(self.url)
        response = urllib2.urlopen(request)

        return response.read()


from ografy.lib.smokesignal.signals.steam import Steam
