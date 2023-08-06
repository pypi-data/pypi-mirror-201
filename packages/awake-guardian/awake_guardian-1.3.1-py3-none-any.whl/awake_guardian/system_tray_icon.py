from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from .config import Icon
from .lang import L


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, aw):
        self.aw = aw
        QSystemTrayIcon.__init__(self, Icon.eyes)
        menu = QMenu()

        self.systray_menu_main = menu.addAction(Icon.inactive, L.PAUSE)
        menu.addSeparator()
        self.systray_menu_settings = menu.addAction(Icon.settings, L.SETTINGS)
        self.systray_menu_exit = menu.addAction(Icon.exit, L.EXIT)
        self.setContextMenu(menu)

        self.systray_menu_main.triggered.connect(aw.timer_toggle)
        self.systray_menu_settings.triggered.connect(aw.dialog_settings.show)
        self.systray_menu_exit.triggered.connect(aw.app.exit)
        self.activated.connect(self.click)
        self.setToolTip(f"{L.TITLE}\n\n{L.HINT}")

    def click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.aw.timer_toggle()
