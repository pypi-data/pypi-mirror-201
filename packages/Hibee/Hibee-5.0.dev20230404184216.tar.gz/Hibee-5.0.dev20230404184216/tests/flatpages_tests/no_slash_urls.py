from hibeeurls import include, path

urlpatterns = [
    path("flatpage", include("hibeecontrib.flatpages.urls")),
]
