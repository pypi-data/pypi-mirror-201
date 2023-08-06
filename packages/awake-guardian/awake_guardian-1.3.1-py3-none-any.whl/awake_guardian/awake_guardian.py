from PySide6.QtCore import QTimer
from datetime import datetime

from .config import Config, Icon
from .hold_dialog import HoldDialog
from .lang import L
from .power_management import SYSTEM_COMMANDS
from .settings_dialog import SettingsDialog
from .sounds import Sound
from .system_tray_icon import SystemTrayIcon
from .user_activity import UserActivity
from .volume_control import VolumeControl


class AwakeGurdian:
    def __init__(self, app):
        self.cfg = Config()
        self.hold_timer = QTimer()
        self.main_timer = QTimer()
        self.main_timer.setInterval(1000)
        self.main_timer.timeout.connect(self.loop)
        self.main_timer.start()

        self.app = app
        self.last_state = 0

        self.dialog_settings = SettingsDialog(self)
        self.dialog_hold = HoldDialog(self)

        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

    def timer_toggle(self):
        if self.main_timer.isActive():
            self.hold()
        else:
            self.resume()

    def resume(self, text=L.PAUSE):
        self.hold_timer.stop()
        self.tray_icon.setIcon(Icon.eyes)
        self.main_timer.start()
        self.tray_icon.systray_menu_main.setText(text)
        self.tray_icon.systray_menu_main.setIcon(Icon.inactive)

    def hold(self, text=L.RESUME):
        self.dialog_hold.show()
        self.tray_icon.setIcon(Icon.inactive)
        self.main_timer.stop()
        self.tray_icon.systray_menu_main.setText(text)
        self.tray_icon.systray_menu_main.setIcon(Icon.eyes)

    def loop(self):
        if self.cfg.t_range:
            t = datetime.now().time()
            tf = self.cfg.t_range_f.toPython()
            tt = self.cfg.t_range_t.toPython()
            if tf > t > tt:
                self.last_state = -1
                self.tray_icon.setIcon(Icon.clock)
                return

        idle_secs = UserActivity.check_idle()

        if self.cfg.power_management:
            if idle_secs >= self.cfg.t_to_event_m * 60 + self.cfg.t_to_event_s:
                UserActivity.idle_secs = 0
                list(SYSTEM_COMMANDS.values())[self.cfg.power_management_action]()

        remind_seconds = self.cfg.t_to_remind_m * 60 + self.cfg.t_to_remind_s
        nag_seconds = self.cfg.t_to_nag_m * 60 + self.cfg.t_to_nag_s
        if self.cfg.remind and idle_secs >= remind_seconds:
            if self.cfg.inc_volume_remind:
                VolumeControl.raise_volume(1)
            self.last_state = 1
            self.remind()
        if self.cfg.nag and idle_secs >= nag_seconds:
            if self.cfg.inc_volume_nag:
                VolumeControl.raise_volume()
            self.last_state = 2
            self.nag()
        if idle_secs < remind_seconds and idle_secs < nag_seconds:
            if self.last_state:
                self.tray_icon.setIcon(Icon.eyes)
                VolumeControl.restore_volume()
                self.last_state = 0

    def remind(self):
        self.tray_icon.setIcon(Icon.beep)
        self.main_timer.setInterval(1000)
        Sound.remind()

    def nag(self):
        self.tray_icon.setIcon(Icon.shout)
        self.main_timer.setInterval(2000)
        Sound.nag()
