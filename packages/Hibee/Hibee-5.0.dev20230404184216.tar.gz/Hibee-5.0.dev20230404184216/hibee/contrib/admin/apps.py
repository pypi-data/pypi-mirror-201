from hibee.apps import AppConfig
from hibee.contrib.admin.checks import check_admin_app, check_dependencies
from hibee.core import checks
from hibee.utils.translation import gettext_lazy as _


class SimpleAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    default_auto_field = "hibee.db.models.AutoField"
    default_site = "hibee.contrib.admin.sites.AdminSite"
    name = "hibee.contrib.admin"
    verbose_name = _("Administration")

    def ready(self):
        checks.register(check_dependencies, checks.Tags.admin)
        checks.register(check_admin_app, checks.Tags.admin)


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default = True

    def ready(self):
        super().ready()
        self.module.autodiscover()
