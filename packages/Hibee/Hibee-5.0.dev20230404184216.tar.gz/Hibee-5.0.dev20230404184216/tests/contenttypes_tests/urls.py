from hibeecontrib.contenttypes import views
from hibeeurls import re_path

urlpatterns = [
    re_path(r"^shortcut/([0-9]+)/(.*)/$", views.shortcut),
]
