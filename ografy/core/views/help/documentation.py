from django.shortcuts import render


def account_creation(request):
    template = 'shared/help/documentation/account.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'account'
    })


def signal_association(request):
    template = 'shared/help/documentation/association.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'association'
    })


def main_app(request):
    template = 'shared/help/documentation/main.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'main'
    })


def settings(request):
    template = 'shared/help/documentation/settings.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'settings'
    })


def pin_to_homepage(request):
    template = 'shared/help/documentation/pinhomepage.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'pinhomepage'
    })


def password(request):
    template = 'shared/help/documentation/password.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'documentation',
        'selected': 'password'
    })
