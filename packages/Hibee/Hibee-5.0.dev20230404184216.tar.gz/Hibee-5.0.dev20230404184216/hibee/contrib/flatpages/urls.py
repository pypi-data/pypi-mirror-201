from hibee.contrib.flatpages import views
from hibee.urls import path

urlpatterns = [
    path("<path:url>", views.flatpage, name="hibee.contrib.flatpages.views.flatpage"),
]
