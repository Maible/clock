#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import sys

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from settings import settings
    # if settings.clock == "analog":
    from clocks import AnalogClock
    clock = AnalogClock(app_settings=settings)
    # else:
    #     clock = PyAnalogClock()
    clock.show()
    sys.exit(app.exec_())
