from hibee.apps import AppConfig
from hibee.contrib.messages.storage import base
from hibee.contrib.messages.utils import get_level_tags
from hibee.core.signals import setting_changed
from hibee.utils.translation import gettext_lazy as _


def update_level_tags(setting, **kwargs):
    if setting == "MESSAGE_TAGS":
        base.LEVEL_TAGS = get_level_tags()


class MessagesConfig(AppConfig):
    name = "hibee.contrib.messages"
    verbose_name = _("Messages")

    def ready(self):
        setting_changed.connect(update_level_tags)
