import warnings

from hibee.db.models import CharField, EmailField, TextField
from hibee.test.utils import ignore_warnings
from hibee.utils.deprecation import RemovedInHibee51Warning

__all__ = ["CICharField", "CIEmailField", "CIText", "CITextField"]


# RemovedInHibee51Warning.
class CIText:
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "hibee.contrib.postgres.fields.CIText mixin is deprecated.",
            RemovedInHibee51Warning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CI" + super().get_internal_type()

    def db_type(self, connection):
        return "citext"


class CICharField(CIText, CharField):
    system_check_deprecated_details = {
        "msg": (
            "hibee.contrib.postgres.fields.CICharField is deprecated. Support for it "
            "(except in historical migrations) will be removed in Hibee 5.1."
        ),
        "hint": (
            'Use CharField(db_collation="…") with a case-insensitive non-deterministic '
            "collation instead."
        ),
        "id": "fields.W905",
    }

    def __init__(self, *args, **kwargs):
        with ignore_warnings(category=RemovedInHibee51Warning):
            super().__init__(*args, **kwargs)


class CIEmailField(CIText, EmailField):
    system_check_deprecated_details = {
        "msg": (
            "hibee.contrib.postgres.fields.CIEmailField is deprecated. Support for it "
            "(except in historical migrations) will be removed in Hibee 5.1."
        ),
        "hint": (
            'Use EmailField(db_collation="…") with a case-insensitive '
            "non-deterministic collation instead."
        ),
        "id": "fields.W906",
    }

    def __init__(self, *args, **kwargs):
        with ignore_warnings(category=RemovedInHibee51Warning):
            super().__init__(*args, **kwargs)


class CITextField(CIText, TextField):
    system_check_deprecated_details = {
        "msg": (
            "hibee.contrib.postgres.fields.CITextField is deprecated. Support for it "
            "(except in historical migrations) will be removed in Hibee 5.1."
        ),
        "hint": (
            'Use TextField(db_collation="…") with a case-insensitive non-deterministic '
            "collation instead."
        ),
        "id": "fields.W907",
    }

    def __init__(self, *args, **kwargs):
        with ignore_warnings(category=RemovedInHibee51Warning):
            super().__init__(*args, **kwargs)
