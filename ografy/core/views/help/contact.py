from django.shortcuts import render


def contact(request):
    template = 'shared/help/contact/contact.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'contact',
    })
