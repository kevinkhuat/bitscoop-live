import django.conf
from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.forms import Form as BaseForm
from django.forms import ModelForm
from django.http import Http404, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import TemplateDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic import View
from hashids import Hashids as Hasher
from mongoengine import Q

from server.contrib.estoolbox import searches
from server.contrib.multiauth.decorators import login_required
from server.contrib.multiauth.models import SignupCode, SignupRequest
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
        return render(request, 'blog.html', {
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

        return render(request, 'contact.html', context)


class ExplorerView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'explore.html', {
            'title': 'Explore'
        })


class FaqView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'faq.html', {
            'title': 'FAQ'
        })


class HelpView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, slug):
        slug = slug.lower()
        template = 'help/{0}.html'.format(slug)

        try:
            return render(request, template, {
                'title': 'Help'
            })
        except TemplateDoesNotExist:
            raise Http404


class HomeView(View, FormMixin):
    class Form(BaseForm):
        email = forms.EmailField()

        def clean(self):
            super().clean()

            user_model = get_user_model()
            email = self.cleaned_data.get('email')

            if email is not None:
                email_count = user_model.objects.by_identifier(email).count()

                if email_count > 0:
                    self.add_error('email', 'Email is in use.')

                email_count = SignupRequest.objects.filter(email__iexact=email).count()

                if email_count > 0:
                    self.add_error('email', 'Email is in use.')

    def get(self, request):
        if request.user.is_authenticated():
            template = 'user/home.html'

            connections = list(ConnectionApi.get(Q(user_id=request.user.id) & Q(auth_status__complete=True)))

            return render(request, template, {
                'connection_count': len(connections)
            })

        else:
            template = 'home-hide.html'

        return render(request, template, {
            'signed_up': request.COOKIES.get('ddfc44b96d0fdd246976ce2d8be2ac4c', False),
            'thanks': request.COOKIES.get('aa4a9dfb1905655f0ef34cb301f095ea', False)
        })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseNotAllowed()

        form = self.get_filled_form(request)

        if form.is_valid():
            signup_request = SignupRequest(**{
                'email': form.cleaned_data.get('email'),
                'ip': request.ip
            })
            signup_request.save()

            response = redirect_by_name('home')
            response.set_cookie('ddfc44b96d0fdd246976ce2d8be2ac4c', True, max_age=2419000)
            response.set_cookie('aa4a9dfb1905655f0ef34cb301f095ea', True, max_age=60)

            return response
        else:
            return render(request, 'home-hide.html', {
                'form': form
            })


class PricingView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'pricing.html', {
            'title': 'Pricing'
        })


class PrivacyView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'privacy.html', {
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

        return render(request, 'providers.html', {
            'title': 'Providers',
            'providers': providers
        })


class SecurityView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'security.html', {
            'title': 'Security'
        })


class SignupView(View, FormMixin):
    class Form(ModelForm):
        password = PasswordField()
        repeated_password = forms.CharField()
        code = forms.CharField()

        class Meta:
            # FIXME: Known 1.7 bug
            # model = get_user_model()
            model = User
            fields = ['email', 'handle', 'first_name', 'last_name']

        def clean_code(self):
            data = self.cleaned_data.get('code')

            # Ideally we'd like to do:
            #
            #      from django.conf import settings
            #
            # And then refer to these settings properties less verbosely, but there appears to be a django bug that
            # prevents this behavior since the direct parent package here is named `settings`. Not sure why.

            hasher = Hasher(
                min_length=django.conf.settings.MULTIAUTH_HASH_MINLENGTH,
                salt=django.conf.settings.MULTIAUTH_HASH_SECRET
            )
            decoded = hasher.decode(data)

            if len(decoded) > 0:
                try:
                    code = SignupCode.objects.get(id=decoded[0])

                    if code.uses > 0:
                        return code
                except SignupCode.DoesNotExist:
                    pass

            raise forms.ValidationError('Invalid signup code.')

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

        return render(request, 'signup.html', {
            'title': 'Sign Up',
            'request_form': True
        })

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseNotAllowed(['GET', 'HEAD', 'OPTIONS'])

        user = None
        code = None
        form = self.get_filled_form(request)

        if form.is_valid():
            user_model = get_user_model()
            form.cleaned_data.pop('repeated_password')
            code = form.cleaned_data.pop('code')
            user = user_model(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(
                identifier=user.email,
                password=form.cleaned_data.get('password')
            )

        if user is None:
            return render(request, 'signup.html', {
                'title': 'Sign Up',
                'form': form,
                'autofocus': 'username' in form.cleaned_data,
                'request_form': False
            })
        else:
            login(request, user)

            SettingsApi.post({
                'user_id': user.id
            })
            searches.create_initial_searches(user.id)

            code.uses -= 1
            code.save()
            code.users.add(user)

            return redirect_by_name('providers')


class SupportView(View):
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
        return render(request, 'team.html', {
            'title': 'Team'
        })


class TermsView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'terms.html', {
            'title': 'Terms of Use'
        })


class UpcomingView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'upcoming.html', {
            'title': 'Upcoming Features'
        })
