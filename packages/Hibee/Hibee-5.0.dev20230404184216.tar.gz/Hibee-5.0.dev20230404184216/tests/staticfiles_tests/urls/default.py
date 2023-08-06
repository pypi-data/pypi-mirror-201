from hibeecontrib.staticfiles import views
from hibeeurls import re_path

urlpatterns = [
    re_path("^static/(?P<path>.*)$", views.serve),
]
