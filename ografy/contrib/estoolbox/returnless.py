import requests


# TODO: Source defaults from settings.py
ES_CERT = None  # ('/path/server.crt', '/path/key')
ES_PROTOCOL = 'https'
ES_SERVER = 'localhost'
ES_PORT = 9200


# Starting of a library to improve performance of ES usage by post/put/patches without waiting for success from the ES box
# TODO: finish/delete/replace
class ESReturnLess:

    def build_uri(self, param_string=None):
        return self.ES_PROTOCOL + '://' + self.ES_SERVER + ':' + str(self.ES_PORT) + param_string

    def get(self, param_string, data):
        return requests.get(self.build_uri(param_string), data=data, cert=self.ES_CERT)

    def es_post(self, param_string, data=None):
        return requests.put(self.build_uri(param_string), data=data, cert=self.ES_CERT)

    def es_put(self, param_string, data=None):
        return requests.patch(self.build_uri(param_string), data=data, cert=self.ES_CERT)

    def es_patch(self, param_string, data=None):
        return requests.patch(self.build_uri(param_string), data=data, cert=self.ES_CERT)

    def delete(self, param_string, data=None):
        return requests.delete(self.build_uri(param_string), data=data, cert=self.ES_CERT)
