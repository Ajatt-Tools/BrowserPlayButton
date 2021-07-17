from typing import Tuple, Any, Optional

from aqt import gui_hooks, mw
from aqt.editor import Editor
from aqt.webview import WebContent

from .common import contains_audio_tag, play_text


def handle_js_messages(handled: Tuple[bool, Any], message: str, context: Any) -> Tuple[bool, Any]:
    if not isinstance(context, Editor) or context.note is None:
        return handled

    if message == 'get_fields_with_audio':
        return True, [contains_audio_tag(context.note[fld['name']]) for fld in context.note.model()["flds"]]

    cmd = message.split(":", maxsplit=1)

    if cmd[0] == "play_field":
        model = context.note.model()
        idx = int(cmd[1])
        fld = model["flds"][idx]
        play_text(context.note[fld['name']])

        return True, None

    return handled


def load_play_button_js(web_content: WebContent, context: Optional[Any]) -> None:
    if isinstance(context, Editor) and not context.addMode:
        addon_package = context.mw.addonManager.addonFromModule(__name__)
        base_path = f"/_addons/{addon_package}/web"

        web_content.css.append(f"{base_path}/play_button.css")
        web_content.js.append(f"{base_path}/play_button.js")


def init():
    mw.addonManager.setWebExports(__name__, r"(web|icons)/.*\.(js|css|png)")
    gui_hooks.webview_did_receive_js_message.append(handle_js_messages)
    gui_hooks.webview_will_set_content.append(load_play_button_js)
