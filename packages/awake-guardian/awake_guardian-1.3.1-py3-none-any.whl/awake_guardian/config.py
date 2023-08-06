from appdirs import AppDirs
from yaml import safe_load, safe_dump
from os import mkdir
from os.path import dirname, isdir
from platform import system
from PySide6.QtCore import QTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

app = QApplication()
path = dirname(__file__)

CONFIG_FILE = "AwakeGuardian"
CONFIG_FILE_EXT = ".conf"

D = "DEFAULT"
LHT = "last_hold_time"
P = "profile"
R = "remind"
N = "nag"
TTRM = "time_to_remind_m"
TTRS = "time_to_remind_s"
TTNM = "time_to_nag_m"
TTNS = "time_to_nag_s"
PM = "power_management"
PMA = "power_management_action"
TTEM = "time_to_event_m"
TTES = "time_to_event_s"
IVR = "increase_volume_remind"
IVN = "increase_volume_nag"
TR = "time_range_active"  # FUTURE: this should be just "time_range" in v2.x, kept for backward compatibility
TRF = "time_range_from"
TRT = "time_range_to"
GS = "geometry_settings"
GH = "geometry_hold"


def defaults(key):
    d = {
        LHT: 15,
        P: 0,
        R: 1,
        N: 1,
        TTRM: 10,
        TTRS: 0,
        TTNM: 15,
        TTNS: 0,
        PM: 0,
        PMA: 1,
        TTEM: 20,
        TTES: 0,
        IVR: 0,
        IVN: 1,
        TR: 1,
        TRF: "20:00:00",
        TRT: "08:00:00",
        GH: None,
        GS: None,
    }
    return key, d[key]


class Icon:
    beep = QIcon(f"{path}/images/beep.png")
    clock = QIcon(f"{path}/images/clock.png")
    exit = QIcon(f"{path}/images/exit.png")
    eyes = QIcon(f"{path}/images/eyes.png")
    inactive = QIcon(f"{path}/images/inactive.png")
    settings = QIcon(f"{path}/images/settings.png")
    shout = QIcon(f"{path}/images/shout.png")


class Audio:
    coin = f"{path}/audio/coin.mp3"
    wilhelm = f"{path}/audio/wilhelm.mp3"


class Config:
    def __init__(self):
        self.config_file = self.setup_config_file()
        self.load_config()

    def setup_config_file(self):
        dirs = AppDirs(CONFIG_FILE)
        config_dir = dirname(dirs.user_config_dir)
        if not isdir(config_dir):
            try:
                mkdir(config_dir)
            except Exception as e:
                raise e
        return f"{dirs.user_config_dir}{CONFIG_FILE_EXT}"

    def set_hold_time(self, minutes):
        self.last_hold_time = minutes
        self.save_config()

    def set_time_to_remind(self, minutes, seconds):
        if minutes is not None:
            self.t_to_remind_m = minutes
        if seconds is not None:
            self.t_to_remind_s = seconds
        self.save_config()

    def set_time_to_nag(self, minutes, seconds):
        if minutes is not None:
            self.t_to_nag_m = minutes
        if seconds is not None:
            self.t_to_nag_s = seconds
        self.save_config()

    def set_time_to_event(self, minutes, seconds):
        if minutes is not None:
            self.t_to_event_m = minutes
        if seconds is not None:
            self.t_to_event_s = seconds
        self.save_config()

    def set_remind(self, value):
        self.remind = int(value)
        self.save_config()

    def set_nag(self, value):
        self.nag = int(value)
        self.save_config()

    def set_power_management(self, value):
        self.power_management = int(value)
        self.save_config()

    def set_power_management_action(self, value):
        self.power_management_action = int(value)
        self.save_config()

    def set_inc_volume_remind(self, value):
        self.inc_volume_remind = value
        self.save_config()

    def set_inc_volume_nag(self, value):
        self.inc_volume_nag = value
        self.save_config()

    def set_time_range(self, value):
        self.t_range = int(value)
        self.save_config()

    def set_time_range_from(self, time):
        self.t_range_f = time
        self.save_config()

    def set_time_range_to(self, time):
        self.t_range_t = time
        self.save_config()

    def set_geometry_settings(self, geometry):
        x = geometry.x()
        y = geometry.y()
        w = geometry.width()
        h = geometry.height()
        self.geometry_settings = f"{x} {y} {w} {h}"
        self.save_config()

    def set_geometry_hold(self, geometry):
        x = geometry.x()
        y = geometry.y()
        w = geometry.width()
        h = geometry.height()
        self.geometry_hold = f"{x} {y} {w} {h}"
        self.save_config()

    def save_config(self):
        settings = {
            P: self.profile,
            R: self.remind,
            N: self.nag,
            TTRM: self.t_to_remind_m,
            TTRS: self.t_to_remind_s,
            TTNM: self.t_to_nag_m,
            TTNS: self.t_to_nag_s,
            IVR: self.inc_volume_remind,
            IVN: self.inc_volume_nag,
            PM: self.power_management,
            PMA: self.power_management_action,
            TTEM: self.t_to_event_m,
            TTES: self.t_to_event_s,
            LHT: self.last_hold_time,
            TR: self.t_range,
            TRF: self.t_range_f.toString(),
            TRT: self.t_range_t.toString(),
            GH: "" if self.geometry_hold is None else self.geometry_hold,
            GS: "" if self.geometry_settings is None else self.geometry_settings,
        }
        with open(self.config_file, "w") as conf_file:
            conf_file.write(safe_dump(settings))

    def clear_config(self):
        open(self.config_file, "w")

    def load_config(self):
        cfg = {}
        try:
            loaded = safe_load(open(self.config_file))
            if loaded:
                cfg = loaded
        except:
            pass

        self.profile = int(cfg.get(*defaults(P)))
        self.remind = int(cfg.get(*defaults(R)))
        self.nag = int(cfg.get(*defaults(N)))

        self.last_hold_time = int(cfg.get(*defaults(LHT)))
        self.t_to_remind_m = int(cfg.get(*defaults(TTRM)))
        self.t_to_remind_s = int(cfg.get(*defaults(TTRS)))
        self.t_to_nag_m = int(cfg.get(*defaults(TTNM)))
        self.t_to_nag_s = int(cfg.get(*defaults(TTNS)))

        self.inc_volume_remind = int(cfg.get(*defaults(IVR)))
        self.inc_volume_nag = int(cfg.get(*defaults(IVN)))
        self.volume = None

        self.power_management = int(cfg.get(*defaults(PM)))
        self.power_management_action = int(cfg.get(*defaults(PMA)))
        self.t_to_event_m = int(cfg.get(*defaults(TTEM)))
        self.t_to_event_s = int(cfg.get(*defaults(TTES)))

        self.t_range = int(cfg.get(*defaults(TR)))
        self.t_range_f = QTime.fromString(cfg.get(*defaults(TRF)))
        self.t_range_t = QTime.fromString(cfg.get(*defaults(TRT)))

        self.geometry_hold = cfg.get(*defaults(GH))
        self.geometry_settings = cfg.get(*defaults(GS))

    def restore_defaults(self):
        self.clear_config()
        self.load_config()
        self.save_config()
