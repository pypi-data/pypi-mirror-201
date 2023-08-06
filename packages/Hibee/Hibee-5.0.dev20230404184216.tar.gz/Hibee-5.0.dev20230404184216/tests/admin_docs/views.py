from hibeecontrib.admindocs.middleware import XViewMiddleware
from hibeehttp import HttpResponse
from hibeeutils.decorators import decorator_from_middleware
from hibeeviews.generic import View

xview_dec = decorator_from_middleware(XViewMiddleware)


def xview(request):
    return HttpResponse()


class XViewClass(View):
    def get(self, request):
        return HttpResponse()


class XViewCallableObject(View):
    def __call__(self, request):
        return HttpResponse()
