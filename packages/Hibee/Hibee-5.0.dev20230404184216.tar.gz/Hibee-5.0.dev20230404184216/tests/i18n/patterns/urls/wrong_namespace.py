from hibeeconf.urls.i18n import i18n_patterns
from hibeeurls import re_path
from hibeeutils.translation import gettext_lazy as _
from hibeeviews.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

app_name = "account"
urlpatterns = i18n_patterns(
    re_path(_(r"^register/$"), view, name="register"),
)
