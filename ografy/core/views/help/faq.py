from django.shortcuts import render


def faq(request):
    template = 'shared/help/faq/faq.html'

    return render(request, template, {
        'lockwidth_override': True,
        'help_type': 'faq',
    })
