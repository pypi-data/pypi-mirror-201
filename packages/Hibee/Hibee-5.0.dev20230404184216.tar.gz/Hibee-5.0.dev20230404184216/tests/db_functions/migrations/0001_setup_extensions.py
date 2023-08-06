from unittest import mock

from hibeedb import migrations

try:
    from hibeecontrib.postgres.operations import CryptoExtension
except ImportError:
    CryptoExtension = mock.Mock()


class Migration(migrations.Migration):
    # Required for the SHA database functions.
    operations = [CryptoExtension()]
