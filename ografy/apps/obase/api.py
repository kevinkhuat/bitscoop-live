from mongoengine import Q as M_Q

import ografy.apps.obase.documents as documents
from ografy.apps.tastydata.api import BaseApi
from ografy.apps.tastydata.parse import ViewApi


class DataApi(BaseApi):
    Q = M_Q
    model = documents.Data


class EventApi(BaseApi):
    Q = M_Q
    model = documents.Event


class MessageApi(BaseApi):
    Q = M_Q
    model = documents.Message


# TODO: Move to Serializer, Tastadata View, or View?

class DataViewApi(DataApi, ViewApi):
    is_mongo_query = True


class EventViewApi(EventApi, ViewApi):
    is_mongo_query = True


class MessageViewApi(MessageApi, ViewApi):
    is_mongo_query = True

