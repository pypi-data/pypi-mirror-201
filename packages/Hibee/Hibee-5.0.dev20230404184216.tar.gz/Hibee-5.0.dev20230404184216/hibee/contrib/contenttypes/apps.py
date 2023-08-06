from hibee.apps import AppConfig
from hibee.contrib.contenttypes.checks import (
    check_generic_foreign_keys,
    check_model_name_lengths,
)
from hibee.core import checks
from hibee.db.models.signals import post_migrate, pre_migrate
from hibee.utils.translation import gettext_lazy as _

from .management import create_contenttypes, inject_rename_contenttypes_operations


class ContentTypesConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.contenttypes"
    verbose_name = _("Content Types")

    def ready(self):
        pre_migrate.connect(inject_rename_contenttypes_operations, sender=self)
        post_migrate.connect(create_contenttypes)
        checks.register(check_generic_foreign_keys, checks.Tags.models)
        checks.register(check_model_name_lengths, checks.Tags.models)
