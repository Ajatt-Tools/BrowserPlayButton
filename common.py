import re

from anki.sound import SoundOrVideoTag
from aqt import sound
from aqt.utils import tooltip
from .config import config

TOOLTIP_ITEM_OFFSET = 14
TOOLTIP_INITIAL_OFFSET = 80
MEDIA_TAG_REGEX = r'\[sound:(.+?\..+?)]'


def truncate_str(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len] + '…'
    else:
        return s


def contains_audio_tag(txt: str):
    return bool(re.match(MEDIA_TAG_REGEX, txt, re.MULTILINE))


def play_text(text: str) -> None:
    results = re.findall(MEDIA_TAG_REGEX, str(text))

    if not results:
        if config['show_tooltips'] is True:
            tooltip("Error: no [sound:XXX]-elements found")
    else:
        if config['show_tooltips'] is True:
            list_items = ''.join([f'<li>{truncate_str(f, max_len=40)}</li>' for f in results])
            y_offset = TOOLTIP_ITEM_OFFSET * len(results) + TOOLTIP_INITIAL_OFFSET
            tooltip(f'<div>Playing files:</div><ol style="margin: 0">{list_items}</ol>', y_offset=y_offset)
        sound.av_player.play_tags([SoundOrVideoTag(filename=f) for f in results])
