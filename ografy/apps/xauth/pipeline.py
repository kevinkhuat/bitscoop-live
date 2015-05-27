import os

from datetime import datetime
from django.shortcuts import redirect

from social.pipeline.partial import partial
from social.pipeline.social_auth import associate_user

from mongoengine import Q

from ografy.apps.core.api import ProviderApi, SignalApi
from ografy.apps.core.documents import Signal


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')


def associate_user_and_signal(backend, uid, user=None, social=None, *args, **kwargs):
    association = associate_user(backend=backend, uid=uid, user=user, social=social, **kwargs)
    if association:
        user = association['user']
        social = association['social']
        provider = ProviderApi.get(Q(backend_name=backend.name))[0]
        signal = Signal(
            user_id=user.id,
            provider=provider,
            name="My " + provider.name + " Account",
            usa_id=social.id,
            connected=True,
            complete=False,
            enabled=False,
            created=datetime.now(),
            updated=datetime.now(),
            last_run=None
        )
        if backend.setting('API_KEY') != None:
            signal.access_token = backend.setting('API_KEY')
        SignalApi.post(signal)

    return association
