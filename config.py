# Copyright: Ren Tatsumoto <tatsu at autistici.org>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from aqt import mw, gui_hooks
from aqt.browser import Browser
from aqt.qt import *

from .consts import ADDON_NAME
from .ajt_common.consts import ADDON_SERIES
from .ajt_common.about_menu import menu_root_entry
from .ajt_common.grab_key import ShortCutGrabButton

config = mw.addonManager.getConfig(__name__)


class SettingsDialog(QDialog):
    toggleables = (
        ('show_toolbar_button', 'Show toolbar button'),
        ('show_play_field_action', 'Show "Play field" context menu action'),
        ('show_play_selection_action', 'Show "Play selection" context menu action'),
        ('show_tooltips', 'Show tooltips'),
        ('autoplay', 'Play audio automatically'),
    )
    contexts = ('both', 'browser', 'add', 'none')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle(f"{ADDON_NAME} Options")
        self.setMinimumSize(320, 240)
        self.bottom_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.shortcut_edit = ShortCutGrabButton(initial_value=config['shortcut'])
        self.context_selector = QComboBox()
        self.checkboxes = self.make_checkboxes()
        self.setLayout(self.setup_layout())
        self.connect_buttons()
        self.load_initial_values()
        self.add_tooltips()

    @classmethod
    def make_checkboxes(cls) -> dict[str, QCheckBox]:
        return {conf_id: QCheckBox(label) for (conf_id, label) in cls.toggleables}

    def setup_layout(self) -> QBoxLayout:
        layout = QVBoxLayout(self)
        layout.addLayout(self.make_upper_layout())
        layout.addLayout(self.make_checkboxes_layout())
        layout.addWidget(
            QLabel("<i>Reopen the Browser window to apply the changes.</i>"),
            alignment=Qt.AlignmentFlag.AlignLeft
        )
        layout.addStretch()
        layout.addWidget(self.bottom_box)
        return layout

    def make_checkboxes_layout(self):
        vbox = QVBoxLayout()
        for widget in self.checkboxes.values():
            vbox.addWidget(widget)
        return vbox

    def make_upper_layout(self):
        layout = QFormLayout()
        layout.addRow("Context", self.context_selector)
        layout.addRow("Shortcut", self.shortcut_edit)
        return layout

    def load_initial_values(self):
        self.context_selector.addItems(context.capitalize() for context in self.contexts)
        self.context_selector.setCurrentText(config.get('context', 'both').capitalize())

        for conf_id, widget in self.checkboxes.items():
            widget.setChecked(config.get(conf_id, True))

    def connect_buttons(self):
        qconnect(self.bottom_box.accepted, self.on_confirm)
        qconnect(self.bottom_box.rejected, self.reject)

    def on_confirm(self):
        config['shortcut'] = self.shortcut_edit.value()
        config['context'] = self.context_selector.currentText().lower()

        for conf_id, widget in self.checkboxes.items():
            config[conf_id] = widget.isChecked()

        mw.addonManager.writeConfig(__name__, config)
        self.accept()

    def add_tooltips(self):
        self.context_selector.setToolTip(
            "When to show play buttons next to field names.\n"
            "\"Browser\" ― only when the Anki Browser is open.\n"
            "\"Add\" ― only when the add dialog is open."
        )
        self.shortcut_edit.setToolTip(
            "Shortcut for the toolbar button.\n"
            "If the toolbar button is disabled, has no effect."
        )
        self.checkboxes['show_tooltips'].setToolTip(
            "Notify what files are being played\n"
            "and show errors if no audio files found."
        )
        self.checkboxes['show_play_field_action'].setToolTip(
            "Add a context menu action to play audio in the selected field."
        )
        self.checkboxes['show_play_selection_action'].setToolTip(
            "Add a context menu action to play audio in the selected text."
        )
        self.checkboxes['show_toolbar_button'].setToolTip(
            "Add a play button to the Editor toolbar\n"
            "to play all audio files on the current note."
        )
        self.checkboxes['autoplay'].setToolTip(
            "Automatically play audio when a note is selected."
        )


def on_open_settings() -> None:
    dialog = SettingsDialog()
    dialog.exec()


def setup_mainwindow_menu():
    root_menu = menu_root_entry()
    action = QAction(f"{ADDON_NAME} Options…", root_menu)
    qconnect(action.triggered, on_open_settings)
    root_menu.addAction(action)


def on_browser_setup_menus(browser: Browser) -> None:
    edit_menu = browser.form.menuEdit
    action = edit_menu.addAction(f"{ADDON_SERIES} {ADDON_NAME} Options…")
    qconnect(action.triggered, on_open_settings)


def init():
    gui_hooks.browser_menus_did_init.append(on_browser_setup_menus)
    mw.addonManager.setConfigAction(__name__, on_open_settings)
    setup_mainwindow_menu()
