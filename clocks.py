import math
import os

from PyQt5.QtCore import QPoint, Qt, QDateTime, QTime, QTimer, QSettings, QRect, QRectF
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class AnalogClock(QMainWindow):
    hourColor = QColor(0x96, 0x72, 0x72, 220)
    minuteColor = QColor(0x40, 0x40, 0x40, 200)
    secondColor = QColor(0x60, 0x60, 0x69, 200)
    whiteShadowColor = QColor(255, 255, 255, 100)
    smokeBackgroundColor = QColor(100, 100, 100, 220)
    helperColor = QColor(211, 211, 211, 75)
    textColor = QColor(18, 18, 19, 255)
    textPanelColor = QColor(238, 238, 238, 200)

    hourHand = QPolygon([
        QPoint(4, 8),
        QPoint(-4, 8),
        QPoint(-4, -40),
        QPoint(4, -40)
    ])
    minuteHand = QPolygon([
        QPoint(3, 8),
        QPoint(-2, 8),
        QPoint(-2, -60),
        QPoint(3, -60)
    ])
    secondHand = QPolygon([
        QPoint(3, 8),
        QPoint(-3, 8),
        QPoint(-3, -70),
        QPoint(3, -70)
    ])

    def updateClock(self):
        time = QTime.currentTime()
        # update every 10 second
        # if time.second() % 10 == 0:
        #     self.update()
        self.update()

    def setWindowFrame(self, withFrame):
        self.withFrame = withFrame
        flags = self.windowFlags()
        if not withFrame:
            flags |= Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        else:
            flags &= ~(Qt.WindowStaysOnBottomHint | Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def __init__(self, parent=None, withFrame=False, settings=None):
        super().__init__(parent)

        # initialize QtTimer
        timer = QTimer(self)
        timer.timeout.connect(self.updateClock)
        timer.start(1000)

        self.setWindowIcon(QIcon(os.path.join(settings.images_dir, "icon.png")))
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.settings = QSettings(settings.app_authors, settings.app_name)

        geometry = self.settings.value('geometry', None)
        if geometry is not None:
            self.restoreGeometry(geometry)
        else:
            # set default window size
            self.resize(100, 100)
        # set frame
        self.setWindowFrame(withFrame)
        # set main window name
        self.setWindowTitle(settings.app_name)
        # set font
        font = QFont()
        font.setStyleHint(QFont.SansSerif)
        font.setFamily('monospace')
        font.setPointSize(12)
        self.font = font
        font = QFont(font)
        font.setPointSize(13)
        self.helperFont = font

    def rotatedPoint(self, x, y, degr):
        theta = degr * math.pi / 180
        s = math.sin(theta)
        c = math.cos(theta)
        return x * c - y * s, x * s + y * c

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        timeDate = QDateTime.currentDateTime()
        timeDateStr = timeDate.toString("HH:mm\nd/MMM")
        time = timeDate.time()
        isAm = time.hour() < 12

        whiteShadowPen = QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        y0 = -90 if 15 <= time.minute() < 45 else 20
        x0 = -90 if 0 <= time.hour() % 12 < 6 else 20
        textPanelRect = QRectF(x0, y0, 69, 29)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # draw clock frame
        painter.setClipping(True)
        p = QPainterPath()
        p.addRect(QRectF(-100, -100, 200, 200))
        p2 = QPainterPath()
        p2.addRect(QRectF(textPanelRect))
        p = p.subtracted(p2)
        painter.setClipPath(p)

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QPoint(0, 0), 99, 99)

        painter.setPen(whiteShadowPen)
        painter.setFont(self.helperFont)
        painter.setBrush(QBrush(self.hourColor))
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -92, i * 360/12)
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(self.helperColor)
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -76, i * 360/12)
            painter.drawText(QRect(x - 10, y - 10, 20, 20), Qt.AlignCenter, "%d" % (i if isAm else i + 12))

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.minuteColor))
        for j in range(0, 60):
            if j % 5 != 0:
                x, y = self.rotatedPoint(0, -92, j * 360/60)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # draw digital clock panel
        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.textPanelColor))
        painter.drawRect(textPanelRect)
        texts = timeDateStr.split('\n')
        painter.setFont(self.font)
        painter.setPen(self.textColor)
        h2 = textPanelRect.height() / 2
        # hour
        # rect = QRect(textPanelRect.left(), textPanelRect.top() + 5, textPanelRect.width(), h2-5)
        # painter.drawText(rect, Qt.AlignCenter, texts[0])
        # date
        rect = QRect(textPanelRect.left(), textPanelRect.top() + h2, textPanelRect.width(), h2-5)
        painter.drawText(rect, Qt.AlignCenter, texts[1])

        # hour pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        # minute pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        # second pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.secondColor))

        painter.save()
        painter.rotate(6.0 * (time.second()))
        painter.drawConvexPolygon(self.secondHand)
        painter.restore()

        painter.end()

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        self.settings.sync()
        super().closeEvent(event)

    def mouseDoubleClickEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)
        self.hide()
        self.setWindowFrame(not self.withFrame)
        self.show()
        self.restoreGeometry(geometry)
