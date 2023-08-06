from hibeeconf.urls.i18n import i18n_patterns
from hibeehttp import HttpResponse
from hibeeurls import path

urlpatterns = i18n_patterns(
    path("exists/", lambda r: HttpResponse()),
)
