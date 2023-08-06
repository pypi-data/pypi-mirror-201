from hibeeurls import include, path

urlpatterns = [
    path("", include([(r"^tuple/$", lambda x: x)])),
]
