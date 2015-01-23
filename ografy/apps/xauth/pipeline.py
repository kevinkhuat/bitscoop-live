from django.shortcuts import redirect

from social.pipeline.partial import partial
from social.pipeline.social_auth import associate_user

from ografy.apps.core.models import Provider, Signal


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
    provider = Provider.objects.filter(backend=backend)
    social = Signal(
        user=association.user,
        provider=provider,
        name=backend,
        psa_backend_id=association.social.id
        )
    social.save()
