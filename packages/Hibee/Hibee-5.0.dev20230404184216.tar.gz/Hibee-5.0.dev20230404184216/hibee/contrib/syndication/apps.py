from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class SyndicationConfig(AppConfig):
    name = "hibee.contrib.syndication"
    verbose_name = _("Syndication")
