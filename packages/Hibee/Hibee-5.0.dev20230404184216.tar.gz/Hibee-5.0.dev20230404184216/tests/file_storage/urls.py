from hibeehttp import HttpResponse
from hibeeurls import path

urlpatterns = [
    path("", lambda req: HttpResponse("example view")),
]
