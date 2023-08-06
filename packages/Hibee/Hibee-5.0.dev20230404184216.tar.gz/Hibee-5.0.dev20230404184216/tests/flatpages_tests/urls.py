from hibeecontrib.flatpages.sitemaps import FlatPageSitemap
from hibeecontrib.sitemaps import views
from hibeeurls import include, path

urlpatterns = [
    path(
        "flatpages/sitemap.xml",
        views.sitemap,
        {"sitemaps": {"flatpages": FlatPageSitemap}},
        name="hibeecontrib.sitemaps.views.sitemap",
    ),
    path("flatpage_root/", include("hibeecontrib.flatpages.urls")),
    path("accounts/", include("hibeecontrib.auth.urls")),
]
