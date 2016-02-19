from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import View
from mongoengine import Q

from server.contrib.multiauth.decorators import login_required
from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import FormMixin
from server.core.api import ConnectionApi, ProviderApi, SettingsApi
from server.core.fields import PasswordField
from server.core.models import User


class BlogView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/blog.html', {
            'title': 'Blog'
        })


class ContactView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        context = {
            'title': 'Contact'
        }

        if request.user.is_authenticated():
            context['email'] = request.user.email

        return render(request, 'core/contact.html', context)


class FaqView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/faq.html', {
            'title': 'FAQ'
        })


class HelpView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, slug):
        slug = slug.lower()
        template = 'core/help/{0}.html'.format(slug)

        try:
            return render(request, template, {
                'title': 'Help'
            })
        except TemplateDoesNotExist:
            raise Http404


class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated():
            template = 'core/user/home.html'

            connections = list(ConnectionApi.get(Q(user_id=request.user.id) & Q(auth_status__complete=True)))

            return render(request, template, {
                'connection_count': len(connections)
            })

        else:
            template = 'core/home.html'
            return render(request, template)


class PricingView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/pricing.html', {
            'title': 'Pricing'
        })


class PrivacyView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/privacy.html', {
            'title': 'Privacy Policy'
        })


class ProvidersView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        providers = list(ProviderApi.get(val=Q(enabled=True)))
        connection_by_user = Q(user_id=request.user.id)
        connections = ConnectionApi.get(val=connection_by_user)

        # FIXME: Make the count happen in the DB
        for provider in providers:
            for connection in connections:
                if provider.provider_number == connection.provider.provider_number and connection.auth_status['complete']:
                    provider.associated_connection = True

                    if hasattr(provider, 'assoc_count'):
                        provider.assoc_count += 1
                    else:
                        provider.assoc_count = 1

        return render(request, 'core/providers.html', {
            'title': 'Providers',
            'providers': providers
        })


class SecurityView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/security.html', {
            'title': 'Security'
        })


class SignupView(View, FormMixin):
    class Form(ModelForm):
        password = PasswordField()
        repeated_password = forms.CharField()

        class Meta:
            # FIXME: Known 1.7 bug
            # model = get_user_model()
            model = User
            fields = ['email', 'handle', 'first_name', 'last_name']

        def clean(self):
            super().clean()

            user_model = get_user_model()
            email = self.cleaned_data.get('email')
            handle = self.cleaned_data.get('handle')
            password = self.cleaned_data.get('password')
            repeated_password = self.cleaned_data.get('repeated_password')

            if password != repeated_password:
                self.add_error('repeated_password', 'Passwords don\'t match.')

            if email is not None:
                email_count = user_model.objects.by_identifier(email).count()

                if email_count > 0:
                    self.add_error('email', 'Email is in use.')

            if handle is not None:
                handle_count = user_model.objects.by_identifier(handle).count()

                if handle_count > 0:
                    self.add_error('handle', 'Handle is in use.')

    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        return render(request, 'core/signup.html', {
            'title': 'Sign Up'
        })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseNotAllowed(['GET', 'HEAD', 'OPTIONS'])

        user = None
        form = self.get_filled_form(request)

        if form.is_valid():
            user_model = get_user_model()
            form.cleaned_data.pop('repeated_password')
            user = user_model(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(identifier=user.email, password=form.cleaned_data.get('password'))
            SettingsApi.post({'user_id': user.id})

        if user is None:
            return render(request, 'core/signup.html', {
                'title': 'Sign Up',
                'form': form,
                'autofocus': 'username' in form.cleaned_data
            })
        else:
            login(request, user)

            return redirect_by_name('home')


class SupportView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('https://docs.google.com/forms/d/1gySynTHyro6Iw3Nl2uiLkDjWF7RHLafr1XimPCXmTGU/viewform?entry.1424639026=' +
                       request.user.full_name + '&entry.720021372=' + request.user.email
                       + '&entry.2009129980&entry.2051677317&entry.1098167114&entry.552209439&&entry.640336011=' + request.user.handle)
        else:
            return HttpResponseRedirect('https://docs.google.com/forms/d/1gySynTHyro6Iw3Nl2uiLkDjWF7RHLafr1XimPCXmTGU/viewform')


class TeamView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/team.html', {
            'title': 'Team'
        })


class TermsView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/terms.html', {
            'title': 'Terms of Use'
        })


class UpcomingView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'core/upcoming.html', {
            'title': 'Upcoming Features'
        })