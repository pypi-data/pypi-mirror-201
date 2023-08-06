from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class SiteMapsConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.sitemaps"
    verbose_name = _("Site Maps")
