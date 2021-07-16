import re
from typing import List

from anki.sound import SoundOrVideoTag
from aqt import gui_hooks
from aqt import sound
from aqt.editor import Editor
from aqt.qt import *
from aqt.utils import tooltip

SHORTCUT = 'alt+m'


def get_addon_path():
    return os.path.dirname(__file__)


def on_play_icon_press(editor: Editor):
    selected_text = editor.web.selectedText()
    if selected_text:
        text = selected_text
    else:
        text = ''.join(editor.note.fields)
    results = re.findall(r'\[sound:(.+?\..+?)]', str(text))

    if not results:
        tooltip("Error: no [sound:XXX]-element found")
    else:
        sound.av_player.play_tags([SoundOrVideoTag(filename=filename) for filename in results])


def on_setup_buttons(buttons: List[str], editor: Editor) -> None:
    icon_path = os.path.join(get_addon_path(), "play.png")
    b = editor.addButton(
        icon_path,
        "play_sound_button",
        on_play_icon_press,
        tip=f"play sound ({SHORTCUT})",
        keys=SHORTCUT,
    )
    buttons.append(b)


gui_hooks.editor_did_init_buttons.append(on_setup_buttons)
