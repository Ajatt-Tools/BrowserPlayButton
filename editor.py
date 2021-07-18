from typing import List

from aqt import gui_hooks
from aqt.editor import Editor, EditorWebView
from aqt.qt import *
from aqt.utils import tooltip

from .common import play_text
from .config import config
from .consts import *


def fetch_note_text(editor: Editor) -> str:
    selected_text = editor.web.selectedText()
    if selected_text:
        return selected_text
    else:
        return ''.join(editor.note.fields)


def get_addon_path() -> str:
    return os.path.dirname(__file__)


def play_field(editor: Editor) -> None:
    if editor.currentField is not None:
        field_content = editor.note.fields[editor.currentField]
        play_text(field_content)
    elif config.get('show_tooltips') is True:
        tooltip("No field selected.")


def append_editor_button(buttons: List[str], editor: Editor) -> None:
    icon_path = os.path.join(get_addon_path(), PLAY_ICON_FILENAME)
    shortcut = config.get('shortcut')
    b = editor.addButton(
        icon_path,
        "play_sound_button",
        lambda e: play_text(fetch_note_text(e)),
        tip=f"play sound ({shortcut if shortcut else 'no shortcut'})",
        keys=shortcut,
    )
    buttons.append(b)


def add_context_menu_item(webview: EditorWebView, menu: QMenu) -> None:
    if config.get('show_play_field_action') is True:
        play_field_action: QAction = menu.addAction("Play field")
        qconnect(play_field_action.triggered, lambda _=False: play_field(webview.editor))

    if config.get('show_play_selection_action') is True:
        play_selection_action: QAction = menu.addAction("Play selection")
        qconnect(play_selection_action.triggered, lambda _=False: play_text(webview.editor.web.selectedText()))


def init():
    gui_hooks.editor_did_init_buttons.append(append_editor_button)
    gui_hooks.editor_will_show_context_menu.append(add_context_menu_item)
