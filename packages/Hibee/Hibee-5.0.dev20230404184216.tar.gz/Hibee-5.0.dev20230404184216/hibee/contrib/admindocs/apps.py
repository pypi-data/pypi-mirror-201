from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class AdminDocsConfig(AppConfig):
    name = "hibee.contrib.admindocs"
    verbose_name = _("Administrative Documentation")
