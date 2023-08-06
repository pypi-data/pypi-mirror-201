from hibee.apps import AppConfig
from hibee.contrib.sites.checks import check_site_id
from hibee.core import checks
from hibee.db.models.signals import post_migrate
from hibee.utils.translation import gettext_lazy as _

from .management import create_default_site


class SitesConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)
        checks.register(check_site_id, checks.Tags.sites)
