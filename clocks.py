import math
import os

from PyQt5.QtCore import QPoint, Qt, QDateTime, QTime, QTimer, QSettings, QRect, QRectF
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QColor, QPainter, QPolygon, QIcon, QFont, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from settingsform import SettingsDialog


class AppClock(QMainWindow):
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

    def setup_main_settings(self, app_settings):
        self.smokeBackgroundColor = QColor(*app_settings.background_color)
        self.hourColor = QColor(*app_settings.hour_color)
        self.minuteColor = QColor(*app_settings.minute_color)
        self.secondColor = QColor(*app_settings.second_color)
        self.whiteShadowColor = QColor(*app_settings.shadow_color)
        self.helperColor = QColor(*app_settings.helper_color)
        self.textColor = QColor(*app_settings.text_color)
        self.textPanelColor = QColor(*app_settings.helper_text_color)

    def __init__(self, parent=None, withFrame=False, app_settings=None):
        super().__init__(parent)
        self.app_settings = app_settings
        self.setup_main_settings(self.app_settings)
        # window title and icon
        self.setWindowIcon(QIcon(os.path.join(app_settings.images_dir, "icon.png")))
        self.setAttribute(Qt.WA_TranslucentBackground)
        # app settings
        self.settings = QSettings(app_settings.app_authors, app_settings.app_name)

        # initialize QtTimer
        timer = QTimer(self)
        timer.timeout.connect(self.updateClock)
        timer.start(1000)

        geometry = self.settings.value('geometry', None)
        if geometry is not None:
            self.restoreGeometry(geometry)
        else:
            # set default window size
            self.resize(100, 100)
        # set frame
        self.setWindowFrame(withFrame)
        # set main window name
        self.setWindowTitle(app_settings.app_name)
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

    def paint_analog_clock(self, event):
        side = min(self.width(), self.height())
        timeDate = QDateTime.currentDateTime()
        timeDateStr = timeDate.toString("HH:mm\nd MMM")
        time = timeDate.time()
        isAm = time.hour() < 12

        whiteShadowPen = QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        y0 = -90 if 15 <= time.minute() < 45 else 20
        x0 = -90 if 0 <= time.hour() % 12 < 6 else 20
        textPanelRect = QRectF(x0, y0, 69, 20)

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

        # draw hours
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
        h2 = textPanelRect.height() / 1
        # hour
        # rect = QRect(textPanelRect.left(), textPanelRect.top() + 5, textPanelRect.width(), h2-5)
        # painter.drawText(rect, Qt.AlignCenter, texts[0])
        # # date
        # rect = QRect(textPanelRect.left(), textPanelRect.top(), textPanelRect.width(), h2-1)
        # painter.drawText(rect, Qt.AlignCenter, texts[1])

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

    def paint_weekday_clock(self, event):
        days = ["Mon", "Tue", "Wed", "Thu", "C.", "Sat", "Sun"]
        side = min(self.width(), self.height())
        timeDate = QDateTime.currentDateTime()
        timeDateStr = timeDate.toString("HH:mm\ndd MMM")
        time = timeDate.time()

        whiteShadowPen = QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        current_day_index = days.index(timeDate.toString("ddd"))
        y0 = -90 if 0 <= current_day_index < 3 else 20
        x0 = -90 if 0 <= current_day_index < 3 else 20
        textPanelRect = QRectF(x0, y0, 69, 40)

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

        # draw days
        painter.setPen(whiteShadowPen)
        painter.setFont(self.helperFont)
        painter.setBrush(QBrush(self.hourColor))
        for i in range(0, 7):
            x, y = self.rotatedPoint(0, -92, i * 360/7)
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(self.helperColor)
        for i in days:
            x, y = self.rotatedPoint(0, -76, days.index(i) * 360/7)
            painter.drawText(QRect(x - 10, y - 10, 20, 20), Qt.AlignCenter, "%s" % i)

        painter.setClipping(False)

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.textPanelColor))
        painter.drawRect(textPanelRect)
        texts = timeDateStr.split('\n')
        painter.setFont(self.font)
        painter.setPen(self.textColor)
        h2 = textPanelRect.height() / 2

        rect = QRect(textPanelRect.left(), textPanelRect.top(), textPanelRect.width(), h2-1)
        painter.drawText(rect, Qt.AlignCenter, texts[0])
        # date
        rect = QRect(textPanelRect.left(), textPanelRect.top() + 18, textPanelRect.width(), h2-1)
        painter.drawText(rect, Qt.AlignCenter, texts[1])

        painter.setPen(whiteShadowPen)
        painter.setBrush(QBrush(self.hourColor))

        painter.save()
        painter.rotate(360.0/7 * current_day_index)
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        painter.end()

    def paintEvent(self, event):
        if self.app_settings.clock == "analog":
            self.paint_analog_clock(event)
        else:
            self.paint_weekday_clock(event)

    def settings_window(self):
        dialog = SettingsDialog(self, app_settings=self.app_settings)
        return dialog.show()

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
        self.settings_window()
