from hibeecontrib.sitemaps import views
from hibeeurls import path

from .http import simple_sitemaps

urlpatterns = [
    path(
        "simple/index.xml",
        views.index,
        {"sitemaps": simple_sitemaps},
        name="hibeecontrib.sitemaps.views.index",
    ),
]
