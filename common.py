# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re

from anki.sound import SoundOrVideoTag
from aqt import sound
from aqt.utils import tooltip

from .ajt_common.media import SOUND_TAG_REGEX, find_sounds
from .config import config
from .consts import *


def truncate_str(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len] + "…"
    else:
        return s


def contains_audio_tag(txt: str):
    return bool(re.search(SOUND_TAG_REGEX, txt))


def play_tooltip(filenames: list[str]):
    list_items = "".join([f"<li><code>{truncate_str(f, max_len=40)}</code></li>" for f in filenames])
    y_offset = TOOLTIP_INITIAL_OFFSET + TOOLTIP_ITEM_OFFSET * len(filenames)
    tooltip(f'<div>Playing files:</div><ol style="margin: 0">{list_items}</ol>', y_offset=y_offset)


def play_text(text: str, quiet: bool = False) -> None:
    results = find_sounds(text)

    if not results:
        if config.show_tooltips is True and not quiet:
            tooltip("Error: no [sound:XXX]-elements found")
    else:
        if config.show_tooltips is True and not quiet:
            play_tooltip(results)
        sound.av_player.play_tags([SoundOrVideoTag(filename=f) for f in results])
