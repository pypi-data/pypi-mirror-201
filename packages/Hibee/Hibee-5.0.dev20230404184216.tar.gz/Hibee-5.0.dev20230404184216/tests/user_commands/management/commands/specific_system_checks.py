from hibee.core.checks import Tags
from hibee.core.management.base import BaseCommand


class Command(BaseCommand):
    requires_system_checks = [Tags.staticfiles, Tags.models]

    def handle(self, *args, **options):
        pass
