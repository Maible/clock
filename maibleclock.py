import math
import sys

from PyQt5.QtCore import QPoint, Qt, QDateTime, QTime, QTimer, QSettings, QRect, QRectF
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    from settings import settings
    if settings.clock == "analog":
        from clocks import AnalogClock
        clock = AnalogClock(settings=settings)
    # else:
    #     clock = PyAnalogClock()
    clock.show()
    sys.exit(app.exec_())
