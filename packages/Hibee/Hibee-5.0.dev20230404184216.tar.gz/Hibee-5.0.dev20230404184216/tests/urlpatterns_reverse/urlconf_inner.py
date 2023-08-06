from hibee.http import HttpResponse
from hibee.template import Context, Template
from hibee.urls import path


def inner_view(request):
    content = Template(
        '{% url "outer" as outer_url %}outer:{{ outer_url }},'
        '{% url "inner" as inner_url %}inner:{{ inner_url }}'
    ).render(Context())
    return HttpResponse(content)


urlpatterns = [
    path("second_test/", inner_view, name="inner"),
]
