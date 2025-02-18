from PySide6.QtCore import QSize
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QLabel, QVBoxLayout

from pyside_app_core import log
from pyside_app_core.services.preferences_service import PreferencesService
from pyside_app_core.ui.standard.main_window import MainToolbarWindow
from pyside_app_core.ui.widgets.connection_manager import ConnectionManager
from pyside_app_core.ui.widgets.core_icon import CoreIcon
from pyside_app_core.ui.widgets.multi_combo_box import MultiComboBox
from pyside_app_core.ui.widgets.preferences_manager import PreferencesDialog


class ToolbarAppMainWindow(MainToolbarWindow):
    def __init__(self) -> None:
        super().__init__()

        # ------------------------------------------------------------------------------
        self.setMinimumSize(QSize(480, 240))

        log.debug(PreferencesService.instance())

        self.tool_bar.setSpacing(10)

    def _build_menus(self) -> None:
        with (
            self._menu_bar.menu("File") as file_menu,
            file_menu.action(
                "Preferences...",
                CoreIcon(":/core/iconoir/settings.svg"),
            ) as self._prefs_action,
        ):
            self._prefs_action.setMenuRole(QAction.MenuRole.PreferencesRole)
            self._prefs_action.triggered.connect(lambda: self.show_app_modal_dialog(PreferencesDialog()))

    def _build_toolbar(self) -> None:
        with self.tool_bar.action(
            "Connect",
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
        ) as plug_action:
            plug_action.setCheckable(True)

        with self.tool_bar.action(
            "Connect",
            CoreIcon(
                ":/core/iconoir/ev-plug-charging.svg",
                ":/core/iconoir/ev-plug-xmark.svg",
            ),
        ) as plug_action:
            plug_action.setCheckable(True)
            plug_action.setChecked(True)

        with self.tool_bar.action(
            "Reload",
            CoreIcon(
                ":/core/iconoir/refresh-circle.svg",
            ),
        ) as reload_action:
            reload_action.setDisabled(True)

        with self.tool_bar.action(
            "Save",
            CoreIcon(
                ":/core/iconoir/floppy-disk.svg",
            ),
        ) as raise_action:

            def _raise() -> None:
                raise Exception("This is a test error")  # noqa

            raise_action.triggered.connect(_raise)

        with self.tool_bar.action(
            "A",
            CoreIcon(
                ":/tb/icons/cube-hole.svg",
            ),
        ):
            pass

        with self.tool_bar.action(
            "Clear Settings",
            CoreIcon(
                ":/tb/icons/one-point-circle.svg",
            ),
        ) as clear_action:
            clear_action.triggered.connect(lambda: PreferencesService.clear_all())

        self.tool_bar.add_stretch()

        self.tool_bar.addAction(self._prefs_action)

        # -----
        _central_layout = QVBoxLayout()
        self.centralWidget().setLayout(_central_layout)

        _heading = QLabel("Examples")
        _central_layout.addWidget(_heading)

        _multi_combo = MultiComboBox[str](placeholder_text="Options", parent=self)
        _multi_combo.addItems(["one", "two", "three", "four"])
        _central_layout.addWidget(_multi_combo)

        _con_mgr = ConnectionManager(parent=self)
        _central_layout.addWidget(_con_mgr)

        _central_layout.addStretch()

        self.statusBar().showMessage("Hi There")
