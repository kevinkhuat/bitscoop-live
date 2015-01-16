import ografy.apps.obase.documents as documents
from ografy.apps.tastydata.api import BaseApi


class DataApi(BaseApi):
    model = documents.Data


class EventApi(BaseApi):
    model = documents.Event


class MessageApi(BaseApi):
    model = documents.Message
