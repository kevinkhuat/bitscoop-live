from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import View

from ografy.apps.core.forms import LoginForm, SignUpForm, UpdateDetailsForm, UpdatePasswordForm
from ografy.util import update
from ografy.util.response import redirect_by_name


class DetailsView(View):
    template_name = 'core/account/details.html'
    title = 'Ografy - Update Details'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DetailsView, self).dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        form = UpdateDetailsForm({
            'email': user.email,
            'handle': user.handle,
            'first_name': user.first_name,
            'last_name': user.last_name
        })

        return render(request, self.template_name, {
            'title': self.title,
            'form': form
        })

    def post(self, request):
        User = get_user_model()

        user = request.user
        form = UpdateDetailsForm(request.POST)
        form.full_clean()

        email = form.cleaned_data.get('email')
        if email is not None:
            email_count = User.objects.filter(email__iexact=email).exclude(id=user.id).count()
            if email_count > 0:
                form.add_error('email', 'Email is in use.')

        handle = form.cleaned_data.get('handle')
        if handle is not None:
            handle_count = User.objects.filter(handle__iexact=handle).exclude(id=user.id).count()
            if handle_count > 0:
                form.add_error('handle', 'Handle is in use.')

        if form.is_valid():
            update(user, form.cleaned_data)
            user.save()

            return redirect_by_name('core_account_index')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'form': form
            })


# Ografy Account specific login/logout
class LoginView(View):
    """
    Directs the user to login view template mapped to the xauth.user model.
    """

    def get(self, request):
        return render(request, 'core/account/login.html', {
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

            return render(request, 'core/account/login.html', {
                'title': 'Ografy - Login',
                'form': form,
                'autofocus': 'identifier' in form.cleaned_data
            })
        else:
            login(request, user)

            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)

            return redirect_by_name('core_index')


class PasswordView(View):
    template_name = 'core/account/password.html'
    title = 'Ografy - Update Password'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PasswordView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {
            'title': self.title
        })

    def post(self, request):
        user = request.user
        form = UpdatePasswordForm(request.POST)
        form.full_clean()

        if not request.user.check_password(form.cleaned_data['password']):
            form.add_error('password', 'Invalid password.')

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.password_date = timezone.now()
            user.save()

            return redirect_by_name('core_account_index')
        else:
            return render(request, self.template_name, {
                'title': self.title,
                'form': form
            })


class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect_by_name('core_index')

        return render(request, 'core/account/signup.html', {
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
            return render(request, 'core/account/signup.html', {
                'title': 'Ografy - Signup',
                'form': form,
                'autofocus': 'username' in form.cleaned_data
            })
        else:
            login(request, user)

            return redirect_by_name('core_index')


@login_required
def index(request):
    return render(request, 'core/account/index.html', {
        'title': 'Ografy - Account'
    })


def logout(request):
    """
    User logout and redirection to the main page.
    """
    auth_logout(request)

    return redirect_by_name('core_index')
