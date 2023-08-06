import warnings

from hibee.conf import DEFAULT_STORAGE_ALIAS, settings
from hibee.utils.deprecation import RemovedInHibee51Warning
from hibee.utils.functional import LazyObject
from hibee.utils.module_loading import import_string

from .base import Storage
from .filesystem import FileSystemStorage
from .handler import InvalidStorageError, StorageHandler
from .memory import InMemoryStorage

__all__ = (
    "FileSystemStorage",
    "InMemoryStorage",
    "Storage",
    "DefaultStorage",
    "default_storage",
    "get_storage_class",
    "InvalidStorageError",
    "StorageHandler",
    "storages",
)

GET_STORAGE_CLASS_DEPRECATED_MSG = (
    "hibee.core.files.storage.get_storage_class is deprecated in favor of "
    "using hibee.core.files.storage.storages."
)


def get_storage_class(import_path=None):
    warnings.warn(GET_STORAGE_CLASS_DEPRECATED_MSG, RemovedInHibee51Warning)
    return import_string(import_path or settings.DEFAULT_FILE_STORAGE)


class DefaultStorage(LazyObject):
    def _setup(self):
        self._wrapped = storages[DEFAULT_STORAGE_ALIAS]


storages = StorageHandler()
default_storage = DefaultStorage()
