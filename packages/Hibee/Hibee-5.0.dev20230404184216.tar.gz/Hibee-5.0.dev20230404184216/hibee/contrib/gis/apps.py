from hibee.apps import AppConfig
from hibee.core import serializers
from hibee.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    default_auto_field = "hibee.db.models.AutoField"
    name = "hibee.contrib.gis"
    verbose_name = _("GIS")

    def ready(self):
        serializers.BUILTIN_SERIALIZERS.setdefault(
            "geojson", "hibee.contrib.gis.serializers.geojson"
        )
