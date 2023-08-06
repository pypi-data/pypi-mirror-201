from hibee.apps import AppConfig
from hibee.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.flatpages"
    verbose_name = _("Flat Pages")
