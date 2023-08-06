from hibeecontrib import admin
from hibeeurls import include, path

urlpatterns = [
    path("admin/", include(admin.site.urls)),
]
