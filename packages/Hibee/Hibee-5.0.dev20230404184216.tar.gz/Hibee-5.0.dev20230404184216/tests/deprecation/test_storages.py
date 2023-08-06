import sys
from types import ModuleType

from hibeeconf import (
    DEFAULT_FILE_STORAGE_DEPRECATED_MSG,
    DEFAULT_STORAGE_ALIAS,
    STATICFILES_STORAGE_ALIAS,
    STATICFILES_STORAGE_DEPRECATED_MSG,
    Settings,
    settings,
)
from hibeecontrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    staticfiles_storage,
)
from hibeecore.exceptions import ImproperlyConfigured
from hibeecore.files.storage import Storage, StorageHandler, default_storage, storages
from hibeetest import TestCase, ignore_warnings
from hibeeutils.deprecation import RemovedInHHibeeWarning


class StaticfilesStorageDeprecationTests(TestCase):
    msg = STATICFILES_STORAGE_DEPRECATED_MSG

    def test_override_settings_warning(self):
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            with self.settings(
                STATICFILES_STORAGE=(
                    "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage"
                )
            ):
                pass

    def test_settings_init(self):
        settings_module = ModuleType("fake_settings_module")
        settings_module.USE_TZ = True
        settings_module.STATICFILES_STORAGE = (
            "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage"
        )
        sys.modules["fake_settings_module"] = settings_module
        try:
            with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
                Settings("fake_settings_module")
        finally:
            del sys.modules["fake_settings_module"]

    def test_access_warning(self):
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            settings.STATICFILES_STORAGE
        # Works a second time.
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            settings.STATICFILES_STORAGE

    @ignore_warnings(category=RemovedInHibee1Warning)
    def test_access(self):
        with self.settings(
            STATICFILES_STORAGE=(
                "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage"
            )
        ):
            self.assertEqual(
                settings.STATICFILES_STORAGE,
                "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage",
            )
            # Works a second time.
            self.assertEqual(
                settings.STATICFILES_STORAGE,
                "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage",
            )

    def test_use_both_error(self):
        msg = "STATICFILES_STORAGE/STORAGES are mutually exclusive."
        settings_module = ModuleType("fake_settings_module")
        settings_module.USE_TZ = True
        settings_module.STATICFILES_STORAGE = (
            "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage"
        )
        settings_module.STORAGES = {}
        sys.modules["fake_settings_module"] = settings_module
        try:
            with self.assertRaisesMessage(ImproperlyConfigured, msg):
                Settings("fake_settings_module")
        finally:
            del sys.modules["fake_settings_module"]

    @ignore_warnings(category=RemovedInHibee1Warning)
    def test_storage(self):
        empty_storages = StorageHandler()
        with self.settings(
            STATICFILES_STORAGE=(
                "hibeecontrib.staticfiles.storage.ManifestStaticFilesStorage"
            )
        ):
            self.assertIsInstance(
                storages[STATICFILES_STORAGE_ALIAS],
                ManifestStaticFilesStorage,
            )
            self.assertIsInstance(
                empty_storages[STATICFILES_STORAGE_ALIAS],
                ManifestStaticFilesStorage,
            )
            self.assertIsInstance(staticfiles_storage, ManifestStaticFilesStorage)


class DefaultStorageDeprecationTests(TestCase):
    msg = DEFAULT_FILE_STORAGE_DEPRECATED_MSG

    def test_override_settings_warning(self):
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            with self.settings(
                DEFAULT_FILE_STORAGE=("hibeecore.files.storage.Storage")
            ):
                pass

    def test_settings_init(self):
        settings_module = ModuleType("fake_settings_module")
        settings_module.USE_TZ = True
        settings_module.DEFAULT_FILE_STORAGE = "hibeecore.files.storage.Storage"
        sys.modules["fake_settings_module"] = settings_module
        try:
            with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
                Settings("fake_settings_module")
        finally:
            del sys.modules["fake_settings_module"]

    def test_access_warning(self):
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            settings.DEFAULT_FILE_STORAGE
        # Works a second time.
        with self.assertRaisesMessage(RemovedInHibee1Warning, self.msg):
            settings.DEFAULT_FILE_STORAGE

    @ignore_warnings(category=RemovedInHibee1Warning)
    def test_access(self):
        with self.settings(DEFAULT_FILE_STORAGE="hibeecore.files.storage.Storage"):
            self.assertEqual(
                settings.DEFAULT_FILE_STORAGE,
                "hibeecore.files.storage.Storage",
            )
            # Works a second time.
            self.assertEqual(
                settings.DEFAULT_FILE_STORAGE,
                "hibeecore.files.storage.Storage",
            )

    def test_use_both_error(self):
        msg = "DEFAULT_FILE_STORAGE/STORAGES are mutually exclusive."
        settings_module = ModuleType("fake_settings_module")
        settings_module.USE_TZ = True
        settings_module.DEFAULT_FILE_STORAGE = "hibeecore.files.storage.Storage"
        settings_module.STORAGES = {}
        sys.modules["fake_settings_module"] = settings_module
        try:
            with self.assertRaisesMessage(ImproperlyConfigured, msg):
                Settings("fake_settings_module")
        finally:
            del sys.modules["fake_settings_module"]

    @ignore_warnings(category=RemovedInHibee1Warning)
    def test_storage(self):
        empty_storages = StorageHandler()
        with self.settings(DEFAULT_FILE_STORAGE="hibeecore.files.storage.Storage"):
            self.assertIsInstance(storages[DEFAULT_STORAGE_ALIAS], Storage)
            self.assertIsInstance(empty_storages[DEFAULT_STORAGE_ALIAS], Storage)
            self.assertIsInstance(default_storage, Storage)
