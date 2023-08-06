from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QFrame,
)

from .autostart import create_autostart, is_autostart, remove_autostart
from .config import system
from .lang import L
from .power_management import SYSTEM_COMMANDS


class SettingsDialog(QDialog):
    def __init__(self, aw):
        def spacer():
            return QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle(L.SETTINGS)

        profile_hbox = QHBoxLayout()
        profile_label = QLabel(L.P)

        self.profile = QComboBox()
        self.profile.addItems(L.LIST_PROFILES)
        profile_hbox.addWidget(profile_label)
        profile_hbox.addWidget(self.profile)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.reminder_group_box = QGroupBox(L.R)
        self.reminder_group_box.setCheckable(True)
        remind_label = QLabel(L.TR)
        self.remind_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.remind_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        self.inc_volume_remind_checkbox = QCheckBox(L.IVR)
        remind_vbox = QVBoxLayout()
        remind_hbox = QHBoxLayout()
        remind_hbox.addWidget(remind_label)
        remind_hbox.addSpacerItem(spacer())
        remind_hbox.addWidget(self.remind_m_spinbox)
        remind_hbox.addWidget(self.remind_s_spinbox)
        remind_vbox.addLayout(remind_hbox)
        remind_vbox.addWidget(self.inc_volume_remind_checkbox)
        self.reminder_group_box.setLayout(remind_vbox)

        self.nag_group_box = QGroupBox(L.N)
        self.nag_group_box.setCheckable(True)
        nag_label = QLabel(L.TN)
        self.nag_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.nag_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        self.inc_volume_nag_checkbox = QCheckBox(L.IVN)
        nag_vbox = QVBoxLayout()
        nag_hbox = QHBoxLayout()
        nag_hbox.addWidget(nag_label)
        nag_hbox.addSpacerItem(spacer())
        nag_hbox.addWidget(self.nag_m_spinbox)
        nag_hbox.addWidget(self.nag_s_spinbox)
        nag_vbox.addLayout(nag_hbox)
        nag_vbox.addWidget(self.inc_volume_nag_checkbox)
        self.nag_group_box.setLayout(nag_vbox)

        self.powermngmt_group_box = QGroupBox(L.PWRMNGMT)
        self.powermngmt_group_box.setCheckable(True)
        powermngmt_layout = QVBoxLayout()
        event_hbox = QHBoxLayout()
        event_label = QLabel(L.TE)
        self.event_m_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_MINUTES)
        self.event_s_spinbox = QSpinBox(maximum=59, suffix=L.SUFFIX_SECONDS)
        event_hbox.addWidget(event_label)
        event_hbox.addSpacerItem(spacer())
        event_hbox.addWidget(self.event_m_spinbox)
        event_hbox.addWidget(self.event_s_spinbox)
        powermngmt_layout.addLayout(event_hbox)
        action_hbox = QHBoxLayout()
        action_label = QLabel(L.PWRMNGMT_ACTION)
        self.pma = QComboBox()
        self.pma.addItems(list(SYSTEM_COMMANDS.keys()))
        action_hbox.addWidget(action_label)
        action_hbox.addWidget(self.pma)
        powermngmt_layout.addLayout(action_hbox)
        self.powermngmt_group_box.setLayout(powermngmt_layout)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)

        s = system()
        if s == "Windows":
            str_autostart = L.WIN_AUTOSTART
            supported_system = True
        elif s == "Linux":
            str_autostart = L.LIN_AUTOSTART
            supported_system = True
        else:
            str_autostart = "Autostart"
            supported_system = False

        self.autostart_checkbox = QCheckBox(str_autostart)
        self.autostart_checkbox.setEnabled(supported_system)

        self.time_range_group_box = QGroupBox(L.WOITM)
        self.time_range_group_box.setCheckable(True)
        time_range_from_label = QLabel(L.TIME_FROM)
        self.time_range_from = QTimeEdit()
        self.time_range_from.setDisplayFormat("hh:mm:ss")
        time_range_to_label = QLabel(L.TIME_TO)
        self.time_range_to = QTimeEdit()
        self.time_range_to.setDisplayFormat("hh:mm:ss")
        time_range_layout = QHBoxLayout()
        time_range_layout.addWidget(time_range_from_label)
        time_range_layout.addWidget(self.time_range_from)
        time_range_layout.addWidget(time_range_to_label)
        time_range_layout.addWidget(self.time_range_to)
        self.time_range_group_box.setLayout(time_range_layout)

        buttons = QDialogButtonBox.Close | QDialogButtonBox.RestoreDefaults
        self.button_box = QDialogButtonBox(buttons)

        layout = QVBoxLayout()
        layout.addLayout(profile_hbox)
        layout.addWidget(line)
        layout.addWidget(self.reminder_group_box)
        layout.addWidget(self.nag_group_box)
        layout.addWidget(self.powermngmt_group_box)
        layout.addWidget(line2)
        layout.addWidget(self.time_range_group_box)
        layout.addWidget(self.autostart_checkbox)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        self.make_connections()
        self.set_values_from_config()

    def set_values_from_config(self):
        self.profile.setCurrentIndex(self.aw.cfg.profile)
        self.remind_m_spinbox.setValue(self.aw.cfg.t_to_remind_m)
        self.remind_s_spinbox.setValue(self.aw.cfg.t_to_remind_s)
        self.nag_m_spinbox.setValue(self.aw.cfg.t_to_nag_m)
        self.nag_s_spinbox.setValue(self.aw.cfg.t_to_nag_s)
        self.inc_volume_remind_checkbox.setChecked(self.aw.cfg.inc_volume_remind)
        self.inc_volume_nag_checkbox.setChecked(self.aw.cfg.inc_volume_nag)
        self.reminder_group_box.setChecked(self.aw.cfg.remind)
        self.nag_group_box.setChecked(self.aw.cfg.nag)
        self.powermngmt_group_box.setChecked(self.aw.cfg.power_management)
        self.event_m_spinbox.setValue(self.aw.cfg.t_to_event_m)
        self.event_s_spinbox.setValue(self.aw.cfg.t_to_event_s)
        self.pma.setCurrentIndex(self.aw.cfg.power_management_action)
        self.autostart_checkbox.setChecked(True)
        self.time_range_group_box.setChecked(self.aw.cfg.t_range)
        self.time_range_from.setTime(self.aw.cfg.t_range_f)
        self.time_range_to.setTime(self.aw.cfg.t_range_t)

    def make_connections(self):
        self.profile.currentIndexChanged.connect(self.set_profile)
        self.remind_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_remind(val, None)
        )
        self.remind_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_remind(None, val)
        )
        self.nag_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_nag(val, None)
        )
        self.nag_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_nag(None, val)
        )
        self.inc_volume_remind_checkbox.stateChanged.connect(
            lambda val: self.aw.cfg.set_inc_volume_remind(val)
        )
        self.inc_volume_nag_checkbox.stateChanged.connect(
            lambda val: self.aw.cfg.set_inc_volume_nag(val)
        )
        self.reminder_group_box.toggled.connect(lambda val: self.aw.cfg.set_remind(val))
        self.nag_group_box.toggled.connect(lambda val: self.aw.cfg.set_nag(val))
        self.powermngmt_group_box.toggled.connect(
            lambda val: self.aw.cfg.set_power_management(val)
        )
        self.event_m_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_event(val, None)
        )
        self.event_s_spinbox.valueChanged.connect(
            lambda val: self.aw.cfg.set_time_to_event(None, val)
        )
        self.pma.activated.connect(
            lambda val: self.aw.cfg.set_power_management_action(val)
        )
        self.autostart_checkbox.stateChanged.connect(
            lambda val: self.toggle_autostart(val)
        )
        self.time_range_group_box.toggled.connect(
            lambda val: self.aw.cfg.set_time_range(val)
        )
        self.time_range_from.timeChanged.connect(
            lambda val: self.set_time_range_from(val)
        )
        self.time_range_to.timeChanged.connect(lambda val: self.set_time_range_to(val))
        self.button_box.button(QDialogButtonBox.Close).clicked.connect(self.hide_dialog)
        self.button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.restore_defaults
        )

    def hide_dialog(self):
        self.aw.cfg.set_geometry_settings(self.geometry())
        self.aw.cfg.save_config()
        self.hide()

    def restore_defaults(self):
        self.aw.cfg.restore_defaults()
        self.set_values_from_config()

    def showEvent(self, event):
        if self.aw.cfg.geometry_settings:
            geometry = [int(s) for s in self.aw.cfg.geometry_settings.split()]
            self.setGeometry(*geometry)
        self.autostart_checkbox.setChecked(is_autostart())
        super(SettingsDialog, self).showEvent(event)

    def toggle_autostart(self, value):
        if value:
            create_autostart()
        else:
            remove_autostart()

    def set_time_range_from(self, val):
        self.aw.cfg.set_time_range_from(val)
        self.time_range_to.setMaximumTime(self.time_range_from.time().addSecs(-1))

    def set_time_range_to(self, val):
        self.aw.cfg.set_time_range_to(val)
        self.time_range_from.setMinimumTime(self.time_range_to.time().addSecs(1))

    def set_profile(self, index):
        self.aw.cfg.profile = index
        if index:
            self.reminder_group_box.setEnabled(False)
            self.reminder_group_box.setChecked(False)
            self.remind_m_spinbox.setValue(59)
            self.remind_s_spinbox.setValue(59)
            self.inc_volume_remind_checkbox.setEnabled(False)
            self.nag_group_box.setEnabled(False)
            self.nag_group_box.setChecked(False)
            self.nag_m_spinbox.setValue(59)
            self.nag_s_spinbox.setValue(59)
            self.inc_volume_nag_checkbox.setEnabled(True)
            self.powermngmt_group_box.setEnabled(False)
            self.pma.setCurrentIndex(1)
            self.event_m_spinbox.setValue(59)
            self.event_s_spinbox.setValue(59)
        else:
            self.reminder_group_box.setEnabled(True)
            self.nag_group_box.setEnabled(True)
            self.powermngmt_group_box.setEnabled(True)
            return

        if index == 1:  # Slow falling asleep
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(10)
            self.remind_s_spinbox.setValue(0)
            self.nag_group_box.setChecked(True)
            self.nag_m_spinbox.setValue(15)
            self.nag_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(False)
        elif index == 2:  # Quick falling asleep
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(5)
            self.remind_s_spinbox.setValue(0)
            self.nag_group_box.setChecked(True)
            self.nag_m_spinbox.setValue(10)
            self.nag_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(False)
        elif index == 3:  # Power saving
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(10)
            self.event_s_spinbox.setValue(0)
        elif index == 4:  # Extreme power saving
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(5)
            self.event_s_spinbox.setValue(0)
        elif index == 5:  # Power saving with remind
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(9)
            self.remind_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(10)
            self.event_s_spinbox.setValue(0)
        elif index == 6:  # Extreme power saving with remind
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(4)
            self.remind_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(5)
            self.event_s_spinbox.setValue(0)
        elif index == 7:  # Power saving with remind and nag
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(8)
            self.remind_s_spinbox.setValue(0)
            self.nag_group_box.setChecked(True)
            self.nag_m_spinbox.setValue(9)
            self.nag_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(10)
            self.event_s_spinbox.setValue(0)
        elif index == 8:  # Extreme power saving with remind and nag
            self.reminder_group_box.setChecked(True)
            self.remind_m_spinbox.setValue(3)
            self.remind_s_spinbox.setValue(0)
            self.nag_group_box.setChecked(True)
            self.nag_m_spinbox.setValue(4)
            self.nag_s_spinbox.setValue(0)
            self.powermngmt_group_box.setChecked(True)
            self.event_m_spinbox.setValue(5)
            self.event_s_spinbox.setValue(0)
