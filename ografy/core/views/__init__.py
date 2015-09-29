from django.contrib.auth import authenticate, get_user_model, login
from django.http import Http404
from django.shortcuts import render
from django.template.loader import TemplateDoesNotExist
from django.views.generic import View
from mongoengine import Q

from ografy.contrib.pytoolbox.django.response import redirect_by_name
from ografy.core.api import ProviderApi, SignalApi
from ografy.core.forms import SignUpForm


class ContactView(View):
    def get(self, request):
        context = {
            'title': 'Contact'
        }

        if request.user.is_authenticated():
            context['email'] = request.user.email

        return render(request, 'core/contact.html', context)


class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('home')

        return render(request, 'core/signup.html', {
            'title': 'Sign Up'
        })

    def post(self, request):
        user_model = get_user_model()

        user = None
        form = SignUpForm(request.POST)
        form.full_clean()
        email = form.cleaned_data.get('email')

        if email is not None:
            email_count = user_model.objects.by_identifier(email).count()

            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')

        if handle is not None:
            handle_count = user_model.objects.by_identifier(handle).count()

            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        if form.is_valid():
            user = user_model(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(identifier=user.email, password=form.cleaned_data.get('password'))

        if user is None:
            return render(request, 'core/signup.html', {
                'title': 'Sign Up',
                'form': form,
                'autofocus': 'username' in form.cleaned_data
            })
        else:
            login(request, user)

            return redirect_by_name('home')


def blog(request):
    return render(request, 'core/blog.html', {
        'title': 'Blog'
    })


def faq(request):
    return render(request, 'core/faq.html', {
        'title': 'FAQ'
    })


def help(request, slug):
    slug = slug.lower()
    template = 'core/help/{0}.html'.format(slug)

    try:
        return render(request, template, {
            'title': 'Help'
        })
    except TemplateDoesNotExist:
        raise Http404


def home(request):
    if request.user.is_authenticated():
        template = 'core/user/home.html'
    else:
        template = 'core/home.html'

    return render(request, template)


def pricing(request):
    return render(request, 'core/pricing.html', {
        'title': 'Pricing'
    })


def privacy(request):
    return render(request, 'core/privacy.html', {
        'title': 'Privacy Policy'
    })


def providers(request):
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


def security(request):
    return render(request, 'core/security.html', {
        'title': 'Security'
    })


def team(request):
    return render(request, 'core/team.html', {
        'title': 'Team'
    })


def terms(request):
    return render(request, 'core/terms.html', {
        'title': 'Terms of Use'
    })


def upcoming(request):
    return render(request, 'core/upcoming.html', {
        'title': 'Upcoming Features'
    })
