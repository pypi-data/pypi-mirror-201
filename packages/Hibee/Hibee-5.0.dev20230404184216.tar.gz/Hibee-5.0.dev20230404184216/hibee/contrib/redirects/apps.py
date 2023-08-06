from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.redirects"
    verbose_name = _("Redirects")
