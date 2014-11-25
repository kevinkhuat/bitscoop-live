from __future__ import unicode_literals

import json

from django.core.serializers import json as djangojson
from django.template.loader import render_to_string
# import msgpack
from tastypie.serializers import Serializer as BaseSerializer

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse


class Serializer(BaseSerializer):
    formats = ['json', 'msgpack', 'urlencoded', 'html']
    content_types = {
        'json': 'application/json',
        'msgpack': 'application/x-msgpack',
        'urlencoded': 'application/x-www-form-urlencoded',
        'html': 'text/html',
    }

    def format_datetime(self, data):
        return data.isoformat()

    def format_date(self, data):
        return data.isoformat()

    def format_time(self, data):
        return data.isoformat()

    def to_json(self, data, options=None, indent=None):
        """
        Given some Python data, produces JSON output.
        """
        options = options or {}
        data = self.to_simple(data, options)

        return djangojson.json.dumps(data, cls=djangojson.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)

    def from_json(self, content):
        """
        Given some JSON data, returns a Python dictionary of the decoded data.
        """
        return json.loads(content)

    # def to_msgpack(self, data, options=None):
    #     return msgpack.packb(self.to_simple(data, options or {}))
    #
    # def from_msgpack(self, content):
    #     return msgpack.unpackb(content)

    def to_urlencoded(self, content):
        pass

    def from_urlencoded(self, data, options=None):
        return urlparse.parse_qs(data, **(options or {}))

    def to_html(self, data, options=None):
        """
        Given some Python data, produces HTML output.
        """
        return render_to_string('tastydata/api.html', {
            'serialized': self.to_json(data, options, indent=4)
        })
