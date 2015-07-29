import hmac
import uuid
from hashlib import md5

from django import forms
from django.conf import settings
from django.core.cache import caches
from django.core.mail import EmailMessage
from django.forms import Form as BaseForm
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import FormMixin
from server.core.fields import PasswordField
from server.core.models import User


class Recover(View, FormMixin):
    success_route = 'password_reset:recover-sent'
    template_name = 'password_reset/recovery_form.html'

    class Form(BaseForm):
        identifier = forms.CharField()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        return render(request, self.template_name, {
            'title': 'Password Reset'
        })

    def post(self, request):
        form = self.get_filled_form(request)

        if form.is_valid():
            try:
                user = User.objects.by_identifier(form.cleaned_data.get('identifier')).first()
            except User.DoesNotExist:
                user = None

            if user:
                signature = hmac.new(uuid.uuid4().bytes, digestmod=md5).hexdigest()
                cache = caches['default']
                cache.set(signature, user.id, settings.PASSWORD_RESET_CACHE_TIMEOUT)

                msg = EmailMessage(to=[user.email])
                msg.template_name = 'password-reset-template'

                msg.global_merge_vars = {
                    'handle': user.identifier,
                    'token': signature,
                }

                msg.send()

        return redirect_by_name(self.success_route)


class RecoverSent(View):
    def get(self, request):
        return render(request, 'password_reset/reset_sent.html', {
            'title': 'Password Reset Sent'
        })


class Reset(View, FormMixin):
    class Form(BaseForm):
        password = PasswordField()
        password_repeated = forms.CharField()

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            password_repeated = cleaned_data.get('password_repeated')

            if password != password_repeated:
                self.add_error('password_repeated', 'Passwords don\'t match.')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, token):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        cache = caches['default']
        user_id = cache.get(token)

        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        return render(request, 'password_reset/reset.html', {
            'title': 'Reset Your Password',
        })

    def post(self, request, token):
        cache = caches['default']
        user_id = cache.get(token)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        form = self.get_filled_form(request)

        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.password_date = timezone.now()
            user.save()

            msg = EmailMessage(to=[user.email])
            msg.template_name = 'password-reset-confirm'

            msg.global_merge_vars = {
                'handle': user.identifier
            }

            msg.send()

            cache.delete(token)

            return redirect_by_name('password_reset:reset-done')
        else:
            return render(request, 'password_reset/reset.html', {
                'title': 'Reset Your Password',
                'form': form
            })


class ResetDone(View):
    def get(self, request):
        return render(request, 'password_reset/recovery_done.html', {
            'title': 'Password Reset Done'
        })
