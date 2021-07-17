import re
from typing import List

from anki.sound import SoundOrVideoTag
from aqt import gui_hooks
from aqt import sound
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import tooltip

SHORTCUT = 'alt+m'
PLAY_ICON_FILENAME = 'icons/play.png'


def get_addon_path() -> str:
    return os.path.dirname(__file__)


def truncate_str(s: str, max_len: int) -> str:
    if len(s) > max_len:
        return s[:max_len] + '…'
    else:
        return s


def fetch_note_text(editor: Editor) -> str:
    selected_text = editor.web.selectedText()
    if selected_text:
        return selected_text
    else:
        return ''.join(editor.note.fields)


def play_text(text: str) -> None:
    results = re.findall(r'\[sound:(.+?\..+?)]', str(text))

    if not results:
        tooltip("Error: no [sound:XXX]-elements found")
    else:
        list_items = ''.join([f'<li>{truncate_str(f, max_len=40)}</li>' for f in results])
        tooltip(f'<div>Playing files:</div><ol style="margin: 0">{list_items}</ol>')
        sound.av_player.play_tags([SoundOrVideoTag(filename=f) for f in results])


def play_field(editor: Editor) -> None:
    field_content = editor.note.fields[editor.currentField]
    play_text(field_content)


def on_setup_buttons(buttons: List[str], editor: Editor) -> None:
    icon_path = os.path.join(get_addon_path(), PLAY_ICON_FILENAME)
    b = editor.addButton(
        icon_path,
        "play_sound_button",
        lambda e: play_text(fetch_note_text(e)),
        tip=f"play sound ({SHORTCUT})",
        keys=SHORTCUT,
    )
    buttons.append(b)


def add_context_menu_item(webview: EditorWebView, menu: QMenu) -> None:
    a: QAction = menu.addAction("Play field")
    qconnect(a.triggered, lambda _=False: play_field(webview.editor))


gui_hooks.editor_did_init_buttons.append(on_setup_buttons)
gui_hooks.editor_will_show_context_menu.append(add_context_menu_item)
