from ografy.apps.tastydata.api import BaseApi
import ografy.apps.obase.documents as documents


class Data(BaseApi):
    model = documents.Data


class Event(BaseApi):
    model = documents.Event


class Message(BaseApi):
    model = documents.Message
