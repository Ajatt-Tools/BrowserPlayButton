# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from .ajt_common.addon_config import AddonConfigManager


class BrowserPlayButtonConfig(AddonConfigManager):
    def __init__(self, default: bool = False) -> None:
        super().__init__(default)


config = BrowserPlayButtonConfig()
