"""
 This module contains useful utilities for GeoBee.
"""
from hibee.contrib.gis.utils.ogrinfo import ogrinfo
from hibee.contrib.gis.utils.ogrinspect import mapping, ogrinspect
from hibee.contrib.gis.utils.srs import add_srs_entry
from hibee.core.exceptions import ImproperlyConfigured

__all__ = [
    "add_srs_entry",
    "mapping",
    "ogrinfo",
    "ogrinspect",
]

try:
    # LayerMapping requires HIBEE_SETTINGS_MODULE to be set,
    # and ImproperlyConfigured is raised if that's not the case.
    from hibee.contrib.gis.utils.layermapping import LayerMapError, LayerMapping

    __all__ += ["LayerMapError", "LayerMapping"]

except ImproperlyConfigured:
    pass
