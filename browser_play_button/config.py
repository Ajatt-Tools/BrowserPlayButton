# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from .ajt_common.addon_config import AddonConfigManager


class BrowserPlayButtonConfig(AddonConfigManager):
    def __init__(self, default: bool = False) -> None:
        super().__init__(default)

    @property
    def show_tooltips(self) -> bool:
        return bool(self["show_tooltips"])

    @property
    def show_play_field_action(self) -> bool:
        return bool(self["show_play_field_action"])

    @property
    def show_play_selection_action(self) -> bool:
        return bool(self["show_play_selection_action"])

    @property
    def show_toolbar_button(self) -> bool:
        return bool(self["show_toolbar_button"])

    @property
    def autoplay(self) -> bool:
        return bool(self["autoplay"])


config = BrowserPlayButtonConfig()
