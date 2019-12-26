import math
import os
from datetime import date

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton, QSizePolicy, QSystemTrayIcon, QMenu, QAction, qApp

from settingsform import SettingsDialog


class AppClock(QMainWindow):
    hourHand = QtGui.QPolygon([
        QtCore.QPoint(4, 8),
        QtCore.QPoint(-4, 8),
        QtCore.QPoint(-4, -40),
        QtCore.QPoint(4, -40)
    ])
    minuteHand = QtGui.QPolygon([
        QtCore.QPoint(3, 8),
        QtCore.QPoint(-2, 8),
        QtCore.QPoint(-2, -60),
        QtCore.QPoint(3, -60)
    ])
    secondHand = QtGui.QPolygon([
        QtCore.QPoint(3, 8),
        QtCore.QPoint(-3, 8),
        QtCore.QPoint(-3, -70),
        QtCore.QPoint(3, -70)
    ])

    def updateClock(self):
        time = QtCore.QTime().currentTime()
        # update every 10 second
        # if time.second() % 10 == 0:
        #     self.update()
        self.update()

    def setWindowFrame(self, with_frame):
        self.withFrame = with_frame
        flags = self.windowFlags()
        if not with_frame:
            flags |= QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        else:
            flags &= ~(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)

    def setup_main_settings(self, app_settings):
        self.smokeBackgroundColor = QtGui.QColor(*app_settings.background_color)
        self.hourColor = QtGui.QColor(*app_settings.hour_color)
        self.minuteColor = QtGui.QColor(*app_settings.minute_color)
        self.secondColor = QtGui.QColor(*app_settings.second_color)
        self.whiteShadowColor = QtGui.QColor(*app_settings.shadow_color)
        self.helperColor = QtGui.QColor(*app_settings.helper_color)
        self.textColor = QtGui.QColor(*app_settings.text_color)
        self.textPanelColor = QtGui.QColor(*app_settings.helper_text_color)

    def __init__(self, parent=None, withFrame=False, app_settings=None):
        super().__init__(parent)
        self.app_settings = app_settings
        self.setup_main_settings(self.app_settings)
        # window title and icon
        self.setWindowIcon(QtGui.QIcon(os.path.join(app_settings.images_dir, "icon.png")))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # minimize to tray
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(os.path.join(app_settings.images_dir, "icon.png")))
        show_action = QAction("Show", self)
        hide_action = QAction("Hide", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)
        hide_action.triggered.connect(self.hide)
        self.tray_icon.activated.connect(self.switch_hide_event)
        tray_menu = QMenu()
        tray_menu.addActions([show_action, hide_action, quit_action])
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        # app settings
        self.settings = QtCore.QSettings(app_settings.app_authors, app_settings.app_name)

        # initialize QtTimer
        timer = QtCore.QTimer(self)
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
        font = QtGui.QFont()
        font.setStyleHint(QtGui.QFont.SansSerif)
        font.setFamily('monospace')
        font.setPointSize(12)
        self.font = font
        font = QtGui.QFont(font)
        font.setPointSize(13)
        self.helperFont = font
        font = QtGui.QFont(font)
        font.setPointSize(10)
        self.dailyFont = font

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

        # schedule buttons
        # button style
        btn_style = """
                    QPushButton {
                        background-color: rgba(0, 0, 0, 0.1);
                        border-radius: 5px;
                        color: #ff0000;}
                    QToolTip {background-color: #ffffff; color: #000000;}
                    """
        # place buttons
        width_factor = self.width() / 100
        btn_size = width_factor * 8
        # place buttons
        # btn 1
        self.events_btn_1 = QPushButton('0', self)
        self.events_btn_1.resize(btn_size, btn_size)
        self.events_btn_1.move(width_factor * 52, width_factor * 2)
        self.events_btn_1.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>test event</p><p>12:10</p></body></html>"""
        )
        self.events_btn_1.setStyleSheet(btn_style)
        # btn2
        self.events_btn_2 = QPushButton('0', self)
        self.events_btn_2.resize(btn_size, btn_size)
        self.events_btn_2.move(width_factor * 60, width_factor * 4)
        self.events_btn_2.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>test event</p><p>12:10</p></body></html>"""
        )
        self.events_btn_2.setStyleSheet(btn_style)
        # btn3
        self.events_btn_3 = QPushButton('2', self)
        self.events_btn_3.resize(btn_size, btn_size)
        self.events_btn_3.move(width_factor * 68, width_factor * 8)
        self.events_btn_3.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>test event</p><p>12:10</p></body></html>"""
        )
        self.events_btn_3.setStyleSheet(btn_style)
        # btn4
        self.events_btn_4 = QPushButton('0', self)
        self.events_btn_4.resize(btn_size, btn_size)
        self.events_btn_4.move(width_factor * 76, width_factor * 13)
        self.events_btn_4.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>test event</p><p>12:10</p></body></html>"""
        )
        self.events_btn_4.setStyleSheet(btn_style)

    def switch_hide_event(self, *_, **__):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def resizeEvent(self, event):
        size = event.size()
        # import code
        # code.interact(local=locals())
        if event.oldSize().width() != size.width():
            # width changed
            size.setHeight(size.width())
            super().resizeEvent(QtGui.QResizeEvent(size, event.oldSize()))
        else:
            # height changed
            size.setWidth(size.height())
            super().resizeEvent(QtGui.QResizeEvent(size, event.oldSize()))
        self.resize(size.width(), size.height())

    def rotatedPoint(self, x, y, degr):
        theta = degr * math.pi / 180
        s = math.sin(theta)
        c = math.cos(theta)
        return x * c - y * s, x * s + y * c

    def paint_analog_clock(self, event):
        side = min(self.width(), self.height())
        timeDate = QtCore.QDateTime.currentDateTime()
        timeDateStr = timeDate.toString("HH:mm\nd MMM")
        time = timeDate.time()
        isAm = time.hour() < 12

        whiteShadowPen = QtGui.QPen(self.whiteShadowColor)
        whiteShadowPen.setJoinStyle(QtCore.Qt.MiterJoin)
        whiteShadowPen.setWidthF(0.9)

        y0 = -90 if 15 <= time.minute() < 45 else 20
        x0 = -90 if 0 <= time.hour() % 12 < 6 else 20
        textPanelRect = QtCore.QRectF(x0, y0, 69, 20)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # draw clock frame
        painter.setClipping(True)
        p = QtGui.QPainterPath()
        p.addRect(QtCore.QRectF(-100, -100, 200, 200))
        p2 = QtGui.QPainterPath()
        p2.addRect(QtCore.QRectF(textPanelRect))
        p = p.subtracted(p2)
        painter.setClipPath(p)

        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QtCore.QPoint(0, 0), 99, 99)

        # draw hours
        painter.setPen(whiteShadowPen)
        painter.setFont(self.helperFont)
        painter.setBrush(QtGui.QBrush(self.hourColor))
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -92, i * 360/12)
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(self.helperColor)
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -76, i * 360/12)
            painter.drawText(QtCore.QRect(x - 10, y - 10, 20, 20), QtCore.Qt.AlignCenter, "%d" % (i if isAm else i + 12))

        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))
        for j in range(0, 60):
            if j % 5 != 0:
                x, y = self.rotatedPoint(0, -92, j * 360/60)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # draw digital clock panel
        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.textPanelColor))
        painter.drawRect(textPanelRect)
        texts = timeDateStr.split('\n')
        painter.setFont(self.font)
        painter.setPen(self.textColor)
        h2 = textPanelRect.height() / 1
        # hour
        # rect = QtCore.QRect(textPanelRect.left(), textPanelRect.top() + 5, textPanelRect.width(), h2-5)
        # painter.drawText(rect, Qt.AlignCenter, texts[0])
        # date
        rect = QtCore.QRect(textPanelRect.left(), textPanelRect.top(), textPanelRect.width(), h2-1)
        painter.drawText(rect, QtCore.Qt.AlignCenter, texts[1])

        # hour pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        # minute pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        # second pointer
        painter.setPen(whiteShadowPen)
        painter.setBrush(QtGui.QBrush(self.secondColor))

        painter.save()
        painter.rotate(6.0 * (time.second()))
        painter.drawConvexPolygon(self.secondHand)
        painter.restore()

        painter.end()

    def paint_weekday_clock(self, event):
        # generate localized days
        timer = QtCore.QDateTime()
        days = []
        base_date = timer.currentDateTime()
        for i in range(7):
            QtCore.QDateTime.setDate(base_date, date(year=2019, month=4, day=i+1))
            days.append(base_date.toString("ddd"))

        # days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        side = min(self.width(), self.height())
        time_date = timer.currentDateTime()
        time_date_str = time_date.toString("HH:mm\ndd MMM")

        white_shadow_pen = QtGui.QPen(self.whiteShadowColor)
        white_shadow_pen.setJoinStyle(QtCore.Qt.MiterJoin)
        white_shadow_pen.setWidthF(0.9)

        current_day_index = days.index(time_date.toString("ddd"))
        y0 = -90 if 0 <= current_day_index < 4 else 20
        x0 = -90 if 0 <= current_day_index < 4 else 20
        text_panel_rect = QtCore.QRectF(x0, y0, 69, 40)

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # draw clock frame
        painter.setClipping(True)
        p = QtGui.QPainterPath()
        p.addRoundedRect(QtCore.QRectF(-100, -100, 200, 200), 10, 10)
        p2 = QtGui.QPainterPath()
        p2.addRoundedRect(QtCore.QRectF(text_panel_rect), 10, 10)
        p = p.subtracted(p2)
        painter.setClipPath(p)

        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QtCore.QPoint(0, 0), 99, 99)

        # draw days
        painter.setPen(white_shadow_pen)
        painter.setFont(self.dailyFont)
        painter.setBrush(QtGui.QBrush(self.hourColor))
        for i in range(0, 7):
            x, y = self.rotatedPoint(0, -92, i * 360/7)
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(self.helperColor)
        for i in days:
            x, y = self.rotatedPoint(0, -76, days.index(i) * 360/7)
            painter.drawText(QtCore.QRect(x - 10, y - 10, 30, 20), QtCore.Qt.AlignCenter, "%s" % i)

        painter.setClipping(False)

        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.textPanelColor))
        painter.drawRoundedRect(text_panel_rect, 10, 10)
        texts = time_date_str.split('\n')
        painter.setFont(self.font)
        painter.setPen(self.textColor)
        h2 = text_panel_rect.height() / 2

        rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top(), text_panel_rect.width(), h2-1)
        painter.drawText(rect, QtCore.Qt.AlignCenter, texts[0])
        # date
        rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top() + 18, text_panel_rect.width(), h2-1)
        painter.drawText(rect, QtCore.Qt.AlignCenter, texts[1])

        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.hourColor))

        painter.save()
        hour_angle = int(time_date.toString("HH")) * (360.0 / 168)
        painter.rotate(360.0/7 * current_day_index + hour_angle)
        painter.drawConvexPolygon(self.secondHand)
        painter.restore()

        painter.end()

    def paintEvent(self, event):
        if self.app_settings.clock == "analog":
            self.paint_analog_clock(event)
        else:
            self.paint_weekday_clock(event)

        width_factor = self.width() / 100
        btn_size = width_factor * 8
        # place buttons
        self.events_btn_1.resize(btn_size, btn_size)
        self.events_btn_1.move(width_factor * 52, width_factor * 1)

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
