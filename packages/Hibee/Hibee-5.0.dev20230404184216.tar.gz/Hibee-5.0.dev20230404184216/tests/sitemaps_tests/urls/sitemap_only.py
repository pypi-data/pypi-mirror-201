from hibeecontrib.sitemaps import views
from hibeeurls import path

urlpatterns = [
    path(
        "sitemap-without-entries/sitemap.xml",
        views.sitemap,
        {"sitemaps": {}},
        name="hibeecontrib.sitemaps.views.sitemap",
    ),
]
