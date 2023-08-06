from hibee.apps import AppConfig
from hibee.contrib.staticfiles.checks import check_finders
from hibee.core import checks
from hibee.utils.translation import gettext_lazy as _


class StaticFilesConfig(AppConfig):
    name = "hibee.contrib.staticfiles"
    verbose_name = _("Static Files")
    ignore_patterns = ["CVS", ".*", "*~"]

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
