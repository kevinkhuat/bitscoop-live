from django.test import SimpleTestCase, TransactionTestCase
from django.core import serializers

from ografy.apps.obase.api import Provider as ProviderApi, Signal as SignalApi
from ografy.apps.obase.api import Data as DataApi, Event as EventApi, Message as MessageApi
from ografy.apps.obase.documents import Message, Data, Event
from ografy.apps.obase.models import Provider, Signal
from ografy.apps.xauth.models import User


class TestOBase(SimpleTestCase):
    fixtures = []

    # def test_OBase_Signal_Api(self):
    #     test_user = User(email='test@test.test', handle='testy')
    #     test_user.save()
    #     test_signal = SignalApi.post(name='Facebook', backend_name='facebook', user=test_user)
    #     test_json = serializers.serialize("json", test_signal)

