from django.shortcuts import redirect
from mongoengine import Q
from social.pipeline.partial import partial
from social.pipeline.social_auth import associate_user

from server.core.api import ConnectionApi


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


def associate_user_and_connection(backend, uid, user=None, social=None, *args, **kwargs):
    # Look up connections from API for current user where connection is not verified or complete.
    connection = ConnectionApi.get(val=Q(user_id=user.id) & (Q(auth_status__complete=False) | Q(auth_status__connected=False)))[0]

    association = associate_user(backend=backend, uid=uid, user=user, social=social, **kwargs)

    if association:
        if ('is_new' in association.keys() and association['is_new']) or ('new_association' in association.keys() and association['new_association']):
            social = association['social']
        else:
            social = backend.strategy.storage.user.get_social_auth_for_user(user=user, provider=backend.name)[0]

    connection['usa_id'] = social.id

    if backend.setting('API_KEY') is not None:
        connection.auth_data['access_token'] = backend.setting('API_KEY')

    connection.save()

    return association
