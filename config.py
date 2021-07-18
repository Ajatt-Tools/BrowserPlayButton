from collections import namedtuple
from typing import List

from aqt import mw, gui_hooks
from aqt.browser import Browser
from aqt.qt import *

from .consts import *

config = mw.addonManager.getConfig(__name__)
Toggleable = namedtuple('Toggleable', 'conf_id, widget')


class SettingsDialog(QDialog):
    toggleables = (
        ('show_toolbar_button', 'Show toolbar button'),
        ('show_play_field_action', 'Show "Play field" context menu action'),
        ('show_play_selection_action', 'Show "Play selection" context menu action'),
        ('show_tooltips', 'Show tooltips'),
    )
    contexts = ('both', 'browser', 'add', 'none')

    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle(f"{ADDON_NAME} settings")
        self.setMinimumSize(200, 80)
        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancel")
        self.shortcut_edit = QLineEdit()
        self.context_selector = QComboBox()
        self.checkboxes = self.make_checkboxes()
        self.setLayout(self.setup_layout())
        self.connect_buttons()
        self.load_initial_values()

    @classmethod
    def make_checkboxes(cls) -> List[Toggleable]:
        return [Toggleable(conf_id, QCheckBox(label)) for (conf_id, label) in cls.toggleables]

    def setup_layout(self) -> QBoxLayout:
        layout = QVBoxLayout(self)
        layout.addLayout(self.make_grid_layout())
        layout.addLayout(self.make_checkboxes_layout())
        layout.addLayout(self.make_bottom_layout())
        return layout

    def make_checkboxes_layout(self):
        vbox = QVBoxLayout()
        for checkbox in self.checkboxes:
            vbox.addWidget(checkbox.widget)
        return vbox

    def make_grid_layout(self):
        gbox = QGridLayout()

        gbox.addWidget(QLabel("Context"), 0, 0)
        gbox.addWidget(self.context_selector, 0, 1)

        gbox.addWidget(QLabel("Shortcut"), 1, 0)
        gbox.addWidget(self.shortcut_edit, 1, 1)

        return gbox

    def make_bottom_layout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.ok_button)
        hbox.addWidget(self.cancel_button)
        hbox.addStretch()
        return hbox

    def load_initial_values(self):
        self.context_selector.addItems((context.capitalize() for context in self.contexts))
        self.context_selector.setCurrentText(config.get('context', 'both').capitalize())
        self.shortcut_edit.setText(config.get('shortcut', 'alt+m'))

        for checkbox in self.checkboxes:
            checkbox.widget.setChecked(config.get(checkbox.conf_id, True))

    def connect_buttons(self):
        qconnect(self.cancel_button.clicked, self.reject)
        qconnect(self.ok_button.clicked, self.on_confirm)

    def on_confirm(self):
        config['shortcut'] = self.shortcut_edit.text()
        config['context'] = self.context_selector.currentText().lower()

        for checkbox in self.checkboxes:
            config[checkbox.conf_id] = checkbox.widget.isChecked()

        mw.addonManager.writeConfig(__name__, config)
        self.accept()


def on_open_settings() -> None:
    dialog = SettingsDialog()
    dialog.exec_()


def on_browser_setup_menus(browser: Browser) -> None:
    edit_menu = browser.form.menuEdit
    action = edit_menu.addAction(f"{ADDON_NAME} settings…")
    qconnect(action.triggered, on_open_settings)


def init():
    gui_hooks.browser_menus_did_init.append(on_browser_setup_menus)
    mw.addonManager.setConfigAction(__name__, on_open_settings)
