from datetime import datetime
from django.shortcuts import redirect

from social.pipeline.partial import partial
from social.pipeline.social_auth import associate_user

from ografy.apps.core.models import Provider, Signal, Permission


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
        provider = Provider.objects.get(backend_name=backend.name)
        permissionsTemplates = provider.permissiontemplate_set.all()
        signal = Signal(
            user=user,
            provider=provider,
            name="My " + backend.name,
            psa_backend_uid=social.uid,
            connected=True,
            complete=False,
            enabled=False,
            created=datetime.now(),
            updated=datetime.now())
        signal.save()

        for temp_permission in permissionsTemplates:
            permission = Permission(
                user=user,
                provider=temp_permission.provider,
                name=temp_permission.name,
                url=temp_permission.url,
                enabled=temp_permission.enabled_by_default,
                permission_template_id=temp_permission.id,
                signal_id=signal.id)
            permission.save()
    return association
