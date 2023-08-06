from hibeeconf.urls.i18n import i18n_patterns
from hibeeurls import path
from hibeeviews.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

urlpatterns = i18n_patterns(
    path("prefixed/", view, name="prefixed"),
)
