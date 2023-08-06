from hibeehttp import HttpResponse


def empty_view(request, *args, **kwargs):
    return HttpResponse()
