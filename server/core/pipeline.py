from django.shortcuts import redirect
from mongoengine import Q
from social.pipeline.partial import partial
from social.pipeline.social_auth import associate_user

from server.core.api import SignalApi


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
    # Look up signals from API for current user where signal is not verified or complete.
    signal = SignalApi.get(val=Q(user_id=user.id) & (Q(complete=False) | Q(connected=False)))[0]

    association = associate_user(backend=backend, uid=uid, user=user, social=social, **kwargs)

    if association:
        social = association['social']

        signal['usa_id'] = social.id

        if backend.setting('API_KEY') is not None:
            signal.access_token = backend.setting('API_KEY')

        signal.save()

    return association
