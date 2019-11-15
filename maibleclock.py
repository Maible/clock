#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import sys

from PyQt5.QtWidgets import QApplication
from clocks import AppClock


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from settings import settings
    clock = AppClock(app_settings=settings)
    clock.show()
    sys.exit(app.exec_())
