from hibeecontrib.flatpages import views
from hibeeurls import path

urlpatterns = [
    path("flatpage/", views.flatpage, {"url": "/hardcoded/"}),
]
