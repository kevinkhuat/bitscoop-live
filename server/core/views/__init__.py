from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.forms import ModelForm
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import render
from django.template.loader import TemplateDoesNotExist
from django.views.generic import View
from mongoengine import Q

from server.contrib.pytoolbox.django.response import redirect_by_name
from server.contrib.pytoolbox.django.views import FormMixin
from server.core.api import ProviderApi, SettingsApi, SignalApi
from server.core.fields import PasswordField
from server.core.models import User


class BlogView(View):
    def get(self, request):
        return render(request, 'core/blog.html', {
            'title': 'Blog'
        })


class ContactView(View):
    def get(self, request):
        context = {
            'title': 'Contact'
        }

        if request.user.is_authenticated():
            context['email'] = request.user.email

        return render(request, 'core/contact.html', context)


class FaqView(View):
    def get(self, request):
        return render(request, 'core/faq.html', {
            'title': 'FAQ'
        })


class HelpView(View):
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
        else:
            template = 'core/home.html'

        return render(request, template)


class PricingView(View):
    def get(self, request):
        return render(request, 'core/pricing.html', {
            'title': 'Pricing'
        })


class PrivacyView(View):
    def get(self, request):
        return render(request, 'core/privacy.html', {
            'title': 'Privacy Policy'
        })


class ProvidersView(View):
    def get(self, request):
        providers = list(ProviderApi.get())
        signal_by_user = Q(user_id=request.user.id)
        signals = SignalApi.get(val=signal_by_user)

        # FIXME: Make the count happen in the DB
        for provider in providers:
            for signal in signals:
                if provider.provider_number == signal.provider.provider_number and signal.complete:
                    provider.associated_signal = True

                    if hasattr(provider, 'assoc_count'):
                        provider.assoc_count += 1
                    else:
                        provider.assoc_count = 1

        return render(request, 'core/providers.html', {
            'title': 'Providers',
            'providers': providers
        })


class SecurityView(View):
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


class TeamView(View):
    def get(self, request):
        return render(request, 'core/team.html', {
            'title': 'Team'
        })


class TermsView(View):
    def get(self, request):
        return render(request, 'core/terms.html', {
            'title': 'Terms of Use'
        })


class UpcomingView(View):
    def get(self, request):
        return render(request, 'core/upcoming.html', {
            'title': 'Upcoming Features'
        })
