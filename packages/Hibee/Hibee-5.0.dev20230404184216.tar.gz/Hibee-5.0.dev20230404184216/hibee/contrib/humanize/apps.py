from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class HumanizeConfig(AppConfig):
    name = "hibee.contrib.humanize"
    verbose_name = _("Humanize")
