from hibeehttp import HttpResponse
from hibeeutils.decorators import method_decorator
from hibeeviews.decorators.common import no_append_slash
from hibeeviews.generic import View


def empty_view(request, *args, **kwargs):
    return HttpResponse()


@no_append_slash
def sensitive_fbv(request, *args, **kwargs):
    return HttpResponse()


@method_decorator(no_append_slash, name="dispatch")
class SensitiveCBV(View):
    def get(self, *args, **kwargs):
        return HttpResponse()
