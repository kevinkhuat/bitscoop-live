from django.shortcuts import render


def _gen_error_view(code, template):
    def view(request):
        return render(request, template, status=code)

    return view


view400 = _gen_error_view(400, 'errors/400.html')
view403 = _gen_error_view(403, 'errors/403.html')
view404 = _gen_error_view(404, 'errors/404.html')
view500 = _gen_error_view(500, 'errors/500.html')
