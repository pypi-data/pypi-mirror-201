from datetime import datetime, timedelta

from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
)

from .lang import L


class HoldDialog(QDialog):
    def __init__(self, aw):
        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.setWindowTitle(L.PAUSE)

        hold_label = QLabel(L.PAUSE_LABEL)
        self.hold_h_spinbox = QSpinBox(
            value=aw.cfg.last_hold_time // 60, maximum=23, suffix=L.SUFFIX_HOURS
        )
        self.hold_m_spinbox = QSpinBox(
            value=aw.cfg.last_hold_time % 60, maximum=59, suffix=L.SUFFIX_MINUTES
        )
        self.hold_h_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_hold_time(val * 60 + self.hold_m_spinbox.value())
        )
        self.hold_m_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_hold_time(self.hold_h_spinbox.value() * 60 + val)
        )

        spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout()
        hold_hbox = QHBoxLayout()
        hold_hbox.addWidget(hold_label)
        hold_hbox.addSpacerItem(spacer1)
        hold_hbox.addWidget(self.hold_h_spinbox)
        hold_hbox.addWidget(self.hold_m_spinbox)

        layout.addLayout(hold_hbox)

        self.button_box = QDialogButtonBox(standardButtons=buttons)
        self.button_box.accepted.connect(self.ok)
        self.button_box.rejected.connect(self.cancel)

        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def ok(self):
        lht = self.aw.cfg.last_hold_time * 60
        t = datetime.now() + timedelta(0, lht)
        self.aw.hold(f'{L.RESUME} ({L.STR_AUTO}: {t.strftime("%H:%M:%S")})')
        self.aw.hold_timer.singleShot(lht * 1000, self.aw.resume)
        self.aw.cfg.set_geometry_hold(self.geometry())
        self.aw.cfg.save_config()
        self.close()

    def cancel(self):
        self.aw.resume()
        self.close()

    def showEvent(self, event):
        if self.aw.cfg.geometry_hold:
            geometry = [int(s) for s in self.aw.cfg.geometry_hold.split()]
            self.setGeometry(*geometry)
        super(HoldDialog, self).showEvent(event)
