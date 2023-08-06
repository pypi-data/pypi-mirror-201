from hibeehttp import HttpResponse
from hibeeurls import path

urlpatterns = [
    path("", lambda request: HttpResponse("root is here")),
]
