from ografy.apps.tastydata.api import BaseApi
import ografy.apps.obase.documents as documents


class DataApi(BaseApi):
    model = documents.Data


class EventApi(BaseApi):
    model = documents.Event


class MessageApi(BaseApi):
    model = documents.Message
