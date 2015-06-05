from django.shortcuts import render


def _gen_error_view(template, title):
    def view(request):
        return render(request, template, {
            'title': title
        })

    return view


view400 = _gen_error_view('core/errors/400.html', 'Ografy - 400 (Bad Request)')
view403 = _gen_error_view('core/errors/403.html', 'Ografy - 403 (Forbidden)')
view404 = _gen_error_view('core/errors/404.html', 'Ografy - 404 (Not Found)')
view500 = _gen_error_view('core/errors/500.html', 'Ografy - 500 (Server Runtime Error)')
