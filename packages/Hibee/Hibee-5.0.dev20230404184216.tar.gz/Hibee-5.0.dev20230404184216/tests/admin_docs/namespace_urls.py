from hibeecontrib import admin
from hibeeurls import include, path

from . import views

backend_urls = (
    [
        path("something/", views.XViewClass.as_view(), name="something"),
    ],
    "backend",
)

urlpatterns = [
    path("admin/doc/", include("hibeecontrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("api/backend/", include(backend_urls, namespace="backend")),
]
