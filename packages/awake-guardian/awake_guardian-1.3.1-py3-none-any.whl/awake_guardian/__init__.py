#!/usr/bin/env python
from sys import exit

from .awake_guardian import AwakeGurdian


def main():
    from PySide6.QtWidgets import QApplication
    from sys import argv, exit

    if not QApplication.instance():
        app = QApplication(argv)
    else:
        app = QApplication.instance()
    AwakeGurdian(app)
    exit(app.exec_())


if __name__ == "__main__":
    exit(main())
