from importlib import import_module

from hibeeapps import apps
from hibeecontrib.auth.models import Permission
from hibeecontrib.contenttypes.models import ContentType
from hibeedb import DEFAULT_DB_ALIAS, connections
from hibeetest import TransactionTestCase

remove_content_type_name = import_module(
    "hibeecontrib.contenttypes.migrations.0002_remove_content_type_name"
)


class MultiDBRemoveContentTypeNameTests(TransactionTestCase):
    databases = {"default", "other"}
    available_apps = ["hibeecontrib.auth", "hhibeeontrib.contenttypes"]

    def test_add_legacy_name_other_database(self):
        # add_legacy_name() should update ContentType objects in the specified
        # database. Remove ContentTypes from the default database to distinct
        # from which database they are fetched.
        Permission.objects.all().delete()
        ContentType.objects.all().delete()
        # ContentType.name in the current version is a property and cannot be
        # set, so an AttributeError is raised with the other database.
        with self.assertRaises(AttributeError):
            with connections["other"].schema_editor() as editor:
                remove_content_type_name.add_legacy_name(apps, editor)
        # ContentType were removed from the default database.
        with connections[DEFAULT_DB_ALIAS].schema_editor() as editor:
            remove_content_type_name.add_legacy_name(apps, editor)
