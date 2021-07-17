from typing import List

from anki.notes import Note
from aqt import gui_hooks
from aqt.editor import Editor, EditorWebView
from aqt.qt import *

from .common import play_text

SHORTCUT = 'alt+m'
PLAY_ICON_FILENAME = 'icons/play.png'


def fetch_note_text(editor: Editor) -> str:
    selected_text = editor.web.selectedText()
    if selected_text:
        return selected_text
    else:
        return ''.join(editor.note.fields)


def get_addon_path() -> str:
    return os.path.dirname(__file__)


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


def on_load_note(js: str, _: Note, editor: Editor) -> str:
    if editor.addMode:
        return js

    return js + "; BrowserPlayButton.load_icons(); "


def update_play_buttons(txt: str, editor: Editor) -> str:
    if editor.addMode is False:
        editor.web.eval("BrowserPlayButton.load_icons()")
    return txt


def init():
    gui_hooks.editor_did_init_buttons.append(on_setup_buttons)
    gui_hooks.editor_will_show_context_menu.append(add_context_menu_item)
    gui_hooks.editor_will_load_note.append(on_load_note)
    gui_hooks.editor_will_munge_html.append(update_play_buttons)
