from django.shortcuts import render


def _gen_error_view(code, template):
    def view(request):
        return render(request, template, status=code)

    return view


view400 = _gen_error_view(400, 'core/errors/400.html')
view403 = _gen_error_view(403, 'core/errors/403.html')
view404 = _gen_error_view(404, 'core/errors/404.html')
view500 = _gen_error_view(500, 'core/errors/500.html')
