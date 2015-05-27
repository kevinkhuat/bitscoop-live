from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout as auth_logout
from django.shortcuts import render
from django.views.generic import View

from ografy.apps.core.forms import LoginForm, SignUpForm
from ografy.util.response import redirect_by_name


# Ografy Account specific login/logout
class LoginView(View):
    """
    Directs the user to login view template mapped to the xauth.user model.
    """

    def get(self, request):
        return render(request, 'core/login.html', {
            'title': 'Ografy - Login'
        })

    def post(self, request):
        user = None
        form = LoginForm(request.POST)
        form.full_clean()

        if form.is_valid():
            user = authenticate(**form.cleaned_data)

        if user is None:
            form.add_error(None, 'Invalid username or password.')

            return render(request, 'core/login.html', {
                'title': 'Ografy - Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })
        else:
            login(request, user)

            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

            return redirect_by_name('core_index')


class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('core_index')

        return render(request, 'core/signup.html', {
            'title': 'Ografy - Sign Up'
        })

    def post(self, request):
        User = get_user_model()

        user = None
        form = SignUpForm(request.POST)
        form.full_clean()

        email = form.cleaned_data.get('email')
        if email is not None:
            email_count = User.objects.by_identifier(email).count()
            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')
        if handle is not None:
            handle_count = User.objects.by_identifier(handle).count()
            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(identifier=user.email, password=form.cleaned_data.get('password'))

        if user is None:
            return render(request, 'core/signup.html', {
                'title': 'Ografy - Signup',
                'form': form,
                'autofocus': 'username' in form.cleaned_data
            })
        else:
            login(request, user)

            return redirect_by_name('core_index')


def index(request):
    if request.user.is_authenticated():
        template = 'core/main/main.html'
        context = {
            'title': 'Ografy - Home'
        }
    else:
        template = 'core/index.html'
        context = {
            'title': 'Ografy'
        }

    return render(request, template, context)


# TODO: Remove, for testing
def signal_scheduler(request):
    if request.user.is_authenticated():
        template='core/main/scheduler.html'
        context= {
            'title': 'Ografy - Signal Scheduler test page',
            'user_id': request.user.id
        }
    else:
        template = 'core/index.html'
        context = {
            'title': 'Ografy'
        }
    return render(request, template, context)


def contact(request):
    return render(request, 'core/contact.html', {
        'title': 'Ografy - Contact'
    })


def logout(request):
    """
    User logout and redirection to the main page.
    """
    auth_logout(request)

    return redirect_by_name('core_index')


def start(request):
    return render(request, 'core/start.html', {
        'title': 'Ografy - Get Started'
    })

