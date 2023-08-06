from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class SessionsConfig(AppConfig):
    name = "hibee.contrib.sessions"
    verbose_name = _("Sessions")
