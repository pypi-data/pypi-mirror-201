from hibeeconf.urls.i18n import i18n_patterns
from hibeehttp import HttpResponse, StreamingHttpResponse
from hibeeurls import path
from hibeeutils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path("simple/", lambda r: HttpResponse()),
    path("streaming/", lambda r: StreamingHttpResponse([_("Yes"), "/", _("No")])),
)
