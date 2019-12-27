import math
import os
from datetime import date, timedelta, datetime

import arrow
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QPushButton, QSizePolicy, QSystemTrayIcon, QMenu, QAction, qApp

from events import MaibleCalendar, EventsDialog
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
        if time.second() % 10 == 0:
            self.update()
        # self.update()

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
        self.event_manager = MaibleCalendar(app_settings)

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
        first_day = arrow.now() - timedelta(days=datetime.now().weekday())
        first_day = first_day.replace(hour=0, minute=0, second=0, microsecond=0)
        # btn 1
        self.events_btn_1 = QPushButton('0', self)
        self.events_btn_1.resize(btn_size, btn_size)
        self.events_btn_1.move(width_factor * 52, width_factor * 2)
        self.events_btn_1.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_1.setStyleSheet(btn_style)
        self.events_btn_1.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn2
        self.events_btn_2 = QPushButton('0', self)
        self.events_btn_2.resize(btn_size, btn_size)
        self.events_btn_2.move(width_factor * 60, width_factor * 4)
        self.events_btn_2.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_2.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_2.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn3
        self.events_btn_3 = QPushButton('0', self)
        self.events_btn_3.resize(btn_size, btn_size)
        self.events_btn_3.move(width_factor * 68, width_factor * 8)
        self.events_btn_3.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_3.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_3.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn4
        self.events_btn_4 = QPushButton('0', self)
        self.events_btn_4.resize(btn_size, btn_size)
        self.events_btn_4.move(width_factor * 76, width_factor * 13)
        self.events_btn_4.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_4.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_4.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn5
        self.events_btn_5 = QPushButton('0', self)
        self.events_btn_5.resize(btn_size, btn_size)
        self.events_btn_5.move(width_factor * 85, width_factor * 24)
        self.events_btn_5.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_5.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_5.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn6
        self.events_btn_6 = QPushButton('0', self)
        self.events_btn_6.resize(btn_size, btn_size)
        self.events_btn_6.move(width_factor * 88, width_factor * 32)
        self.events_btn_6.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_6.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_6.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn7
        self.events_btn_7 = QPushButton('0', self)
        self.events_btn_7.resize(btn_size, btn_size)
        self.events_btn_7.move(width_factor * 91, width_factor * 41)
        self.events_btn_7.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_7.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_7.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn8
        self.events_btn_8 = QPushButton('0', self)
        self.events_btn_8.resize(btn_size, btn_size)
        self.events_btn_8.move(width_factor * 91, width_factor * 50)
        self.events_btn_8.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_8.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_8.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn9
        self.events_btn_9 = QPushButton('0', self)
        self.events_btn_9.resize(btn_size, btn_size)
        self.events_btn_9.move(width_factor * 88, width_factor * 62)
        self.events_btn_9.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_9.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_9.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn10
        self.events_btn_10 = QPushButton('0', self)
        self.events_btn_10.resize(btn_size, btn_size)
        self.events_btn_10.move(width_factor * 84, width_factor * 70)
        self.events_btn_10.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_10.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_10.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn11
        self.events_btn_11 = QPushButton('0', self)
        self.events_btn_11.resize(btn_size, btn_size)
        self.events_btn_11.move(width_factor * 78, width_factor * 77)
        self.events_btn_11.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_11.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_11.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn12
        self.events_btn_12 = QPushButton('0', self)
        self.events_btn_12.resize(btn_size, btn_size)
        self.events_btn_12.move(width_factor * 71, width_factor * 84)
        self.events_btn_12.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_12.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_12.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn13
        self.events_btn_13 = QPushButton('0', self)
        self.events_btn_13.resize(btn_size, btn_size)
        self.events_btn_13.move(width_factor * 59, width_factor * 89)
        self.events_btn_13.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_13.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_13.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn14
        self.events_btn_14 = QPushButton('0', self)
        self.events_btn_14.resize(btn_size, btn_size)
        self.events_btn_14.move(width_factor * 50, width_factor * 91)
        self.events_btn_14.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_14.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_14.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn15
        self.events_btn_15 = QPushButton('0', self)
        self.events_btn_15.resize(btn_size, btn_size)
        self.events_btn_15.move(width_factor * 41, width_factor * 91)
        self.events_btn_15.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_15.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_15.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn16
        self.events_btn_16 = QPushButton('0', self)
        self.events_btn_16.resize(btn_size, btn_size)
        self.events_btn_16.move(width_factor * 33, width_factor * 89)
        self.events_btn_16.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_16.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_16.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn17
        self.events_btn_17 = QPushButton('0', self)
        self.events_btn_17.resize(btn_size, btn_size)
        self.events_btn_17.move(width_factor * 21, width_factor * 83)
        self.events_btn_17.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_17.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_17.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn18
        self.events_btn_18 = QPushButton('0', self)
        self.events_btn_18.resize(btn_size, btn_size)
        self.events_btn_18.move(width_factor * 14, width_factor * 78)
        self.events_btn_18.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_18.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_18.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn19
        self.events_btn_19 = QPushButton('0', self)
        self.events_btn_19.resize(btn_size, btn_size)
        self.events_btn_19.move(width_factor * 9, width_factor * 70)
        self.events_btn_19.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_19.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_19.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn20
        self.events_btn_20 = QPushButton('0', self)
        self.events_btn_20.resize(btn_size, btn_size)
        self.events_btn_20.move(width_factor * 4, width_factor * 62)
        self.events_btn_20.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_20.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_20.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn21
        self.events_btn_21 = QPushButton('0', self)
        self.events_btn_21.resize(btn_size, btn_size)
        self.events_btn_21.move(width_factor * 1, width_factor * 50)
        self.events_btn_21.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_21.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_21.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn22
        self.events_btn_22 = QPushButton('0', self)
        self.events_btn_22.resize(btn_size, btn_size)
        self.events_btn_22.move(width_factor * 1, width_factor * 41)
        self.events_btn_22.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_22.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_22.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn23
        self.events_btn_23 = QPushButton('0', self)
        self.events_btn_23.resize(btn_size, btn_size)
        self.events_btn_23.move(width_factor * 4, width_factor * 32)
        self.events_btn_23.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_23.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_23.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn24
        self.events_btn_24 = QPushButton('0', self)
        self.events_btn_24.resize(btn_size, btn_size)
        self.events_btn_24.move(width_factor * 7, width_factor * 24)
        self.events_btn_24.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_24.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_24.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn25
        self.events_btn_25 = QPushButton('0', self)
        self.events_btn_25.resize(btn_size, btn_size)
        self.events_btn_25.move(width_factor * 16, width_factor * 12)
        self.events_btn_25.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_25.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_25.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn26
        self.events_btn_26 = QPushButton('0', self)
        self.events_btn_26.resize(btn_size, btn_size)
        self.events_btn_26.move(width_factor * 24, width_factor * 6)
        self.events_btn_26.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_26.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_26.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn27
        self.events_btn_27 = QPushButton('0', self)
        self.events_btn_27.resize(btn_size, btn_size)
        self.events_btn_27.move(width_factor * 32, width_factor * 3)
        self.events_btn_27.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_27.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_27.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )
        # btn28
        self.events_btn_28 = QPushButton('0', self)
        self.events_btn_28.resize(btn_size, btn_size)
        self.events_btn_28.move(width_factor * 40, width_factor * 1)
        self.events_btn_28.setToolTip(
            """<html><head/><body style="background-color: #aaaaaa;"><p>No Events</p></body></html>"""
        )
        self.events_btn_28.setStyleSheet(btn_style)
        first_day = first_day + timedelta(hours=6)
        self.events_btn_28.clicked.connect(
            self.make_event_button_action(arrow.get(first_day), first_day + timedelta(hours=6))
        )

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

    def rotatedPoint(self, x, y, degree):
        theta = degree * math.pi / 180
        s = math.sin(theta)
        c = math.cos(theta)
        return x * c - y * s, x * s + y * c

    def paint_analog_clock(self, event):
        side = min(self.width(), self.height())
        time_date = QtCore.QDateTime().currentDateTime()
        time_date_str = time_date.toString("HH:mm\nd MMM")
        time = time_date.time()
        is_am = time.hour() < 12

        white_shadow_pen = QtGui.QPen(self.whiteShadowColor)
        white_shadow_pen.setJoinStyle(QtCore.Qt.MiterJoin)
        white_shadow_pen.setWidthF(0.9)

        y0 = -90 if 15 <= time.minute() < 45 else 20
        x0 = -90 if 0 <= time.hour() % 12 < 6 else 20
        text_panel_rect = QtCore.QRectF(x0, y0, 69, 20)

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
        p2.addRect(QtCore.QRectF(text_panel_rect))
        p = p.subtracted(p2)
        painter.setClipPath(p)

        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.smokeBackgroundColor))
        painter.drawEllipse(QtCore.QPoint(0, 0), 99, 99)

        # draw hours
        painter.setPen(white_shadow_pen)
        painter.setFont(self.helperFont)
        painter.setBrush(QtGui.QBrush(self.hourColor))
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -92, i * 360/12)
            painter.drawEllipse(x - 3, y - 3, 6, 6)
        painter.setPen(self.helperColor)
        for i in range(0, 12):
            x, y = self.rotatedPoint(0, -76, i * 360/12)
            painter.drawText(QtCore.QRect(x - 10, y - 10, 20, 20), QtCore.Qt.AlignCenter, "%d" % (i if is_am else i + 12))

        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))
        for j in range(0, 60):
            if j % 5 != 0:
                x, y = self.rotatedPoint(0, -92, j * 360/60)
                painter.drawEllipse(x - 1, y - 1, 2, 2)
        painter.setClipping(False)

        # draw digital clock panel
        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.textPanelColor))
        painter.drawRect(text_panel_rect)
        texts = time_date_str.split('\n')
        painter.setFont(self.font)
        painter.setPen(self.textColor)
        h2 = text_panel_rect.height() / 1
        # hour
        # rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top() + 5, text_panel_rect.width(), h2-5)
        # painter.drawText(rect, Qt.AlignCenter, texts[0])
        # date
        rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top(), text_panel_rect.width(), h2-1)
        painter.drawText(rect, QtCore.Qt.AlignCenter, texts[1])

        # hour pointer
        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.hourColor))

        painter.save()
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        painter.drawConvexPolygon(self.hourHand)
        painter.restore()

        # minute pointer
        painter.setPen(white_shadow_pen)
        painter.setBrush(QtGui.QBrush(self.minuteColor))

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(self.minuteHand)
        painter.restore()

        # second pointer
        painter.setPen(white_shadow_pen)
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
        # p2 = QtGui.QPainterPath()
        # p2.addRoundedRect(QtCore.QRectF(text_panel_rect), 10, 10)
        # p = p.subtracted(p2)
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

        # show helper window
        # painter.setPen(white_shadow_pen)
        # painter.setBrush(QtGui.QBrush(self.textPanelColor))
        # painter.drawRoundedRect(text_panel_rect, 10, 10)
        # texts = time_date_str.split('\n')
        # painter.setFont(self.font)
        # painter.setPen(self.textColor)
        # h2 = text_panel_rect.height() / 2
        #
        # rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top(), text_panel_rect.width(), h2-1)
        # painter.drawText(rect, QtCore.Qt.AlignCenter, texts[0])
        # date
        # rect = QtCore.QRect(text_panel_rect.left(), text_panel_rect.top() + 18, text_panel_rect.width(), h2-1)
        # painter.drawText(rect, QtCore.Qt.AlignCenter, texts[1])

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
        first_day = arrow.now() - timedelta(days=datetime.now().weekday())
        first_day = first_day.replace(hour=0, minute=0, second=0, microsecond=0)
        # place buttons
        # btn1
        self.events_btn_1.resize(btn_size, btn_size)
        self.events_btn_1.move(width_factor * 52, width_factor * 1)
        events = self.event_manager.events_between(arrow.get(first_day), first_day + timedelta(hours=6))
        self.events_btn_1.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_1.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn2
        first_day = first_day + timedelta(hours=6)
        self.events_btn_2.resize(btn_size, btn_size)
        self.events_btn_2.move(width_factor * 60, width_factor * 4)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_2.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_2.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn3
        first_day = first_day + timedelta(hours=6)
        self.events_btn_3.resize(btn_size, btn_size)
        self.events_btn_3.move(width_factor * 68, width_factor * 8)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_3.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_3.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn4
        first_day = first_day + timedelta(hours=6)
        self.events_btn_4.resize(btn_size, btn_size)
        self.events_btn_4.move(width_factor * 76, width_factor * 13)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_4.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_4.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn5
        first_day = first_day + timedelta(hours=6)
        self.events_btn_5.resize(btn_size, btn_size)
        self.events_btn_5.move(width_factor * 85, width_factor * 24)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_5.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_5.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn6
        first_day = first_day + timedelta(hours=6)
        self.events_btn_6.resize(btn_size, btn_size)
        self.events_btn_6.move(width_factor * 88, width_factor * 32)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_6.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_6.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn7
        first_day = first_day + timedelta(hours=6)
        self.events_btn_7.resize(btn_size, btn_size)
        self.events_btn_7.move(width_factor * 91, width_factor * 41)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_7.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_7.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn8
        first_day = first_day + timedelta(hours=6)
        self.events_btn_8.resize(btn_size, btn_size)
        self.events_btn_8.move(width_factor * 91, width_factor * 50)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_8.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_8.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn9
        first_day = first_day + timedelta(hours=6)
        self.events_btn_9.resize(btn_size, btn_size)
        self.events_btn_9.move(width_factor * 88, width_factor * 62)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_9.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_9.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn10
        first_day = first_day + timedelta(hours=6)
        self.events_btn_10.resize(btn_size, btn_size)
        self.events_btn_10.move(width_factor * 84, width_factor * 70)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_10.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_10.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn11
        first_day = first_day + timedelta(hours=6)
        self.events_btn_11.resize(btn_size, btn_size)
        self.events_btn_11.move(width_factor * 78, width_factor * 77)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_11.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_11.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn12
        first_day = first_day + timedelta(hours=6)
        self.events_btn_12.resize(btn_size, btn_size)
        self.events_btn_12.move(width_factor * 71, width_factor * 84)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_12.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_12.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn13
        first_day = first_day + timedelta(hours=6)
        self.events_btn_13.resize(btn_size, btn_size)
        self.events_btn_13.move(width_factor * 59, width_factor * 89)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_13.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_13.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn14
        first_day = first_day + timedelta(hours=6)
        self.events_btn_14.resize(btn_size, btn_size)
        self.events_btn_14.move(width_factor * 50, width_factor * 91)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_14.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_14.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn15
        first_day = first_day + timedelta(hours=6)
        self.events_btn_15.resize(btn_size, btn_size)
        self.events_btn_15.move(width_factor * 41, width_factor * 91)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_15.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_15.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn16
        first_day = first_day + timedelta(hours=6)
        self.events_btn_16.resize(btn_size, btn_size)
        self.events_btn_16.move(width_factor * 33, width_factor * 89)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_16.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_16.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn17
        first_day = first_day + timedelta(hours=6)
        self.events_btn_17.resize(btn_size, btn_size)
        self.events_btn_17.move(width_factor * 21, width_factor * 83)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_17.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_17.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn18
        first_day = first_day + timedelta(hours=6)
        self.events_btn_18.resize(btn_size, btn_size)
        self.events_btn_18.move(width_factor * 14, width_factor * 78)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_18.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_18.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn19
        first_day = first_day + timedelta(hours=6)
        self.events_btn_19.resize(btn_size, btn_size)
        self.events_btn_19.move(width_factor * 9, width_factor * 70)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_19.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_19.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn20
        first_day = first_day + timedelta(hours=6)
        self.events_btn_20.resize(btn_size, btn_size)
        self.events_btn_20.move(width_factor * 4, width_factor * 62)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_20.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_20.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn21
        first_day = first_day + timedelta(hours=6)
        self.events_btn_21.resize(btn_size, btn_size)
        self.events_btn_21.move(width_factor * 1, width_factor * 50)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_21.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_21.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn22
        first_day = first_day + timedelta(hours=6)
        self.events_btn_22.resize(btn_size, btn_size)
        self.events_btn_22.move(width_factor * 1, width_factor * 41)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_22.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_22.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn23
        first_day = first_day + timedelta(hours=6)
        self.events_btn_23.resize(btn_size, btn_size)
        self.events_btn_23.move(width_factor * 4, width_factor * 32)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_23.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_23.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn24
        first_day = first_day + timedelta(hours=6)
        self.events_btn_24.resize(btn_size, btn_size)
        self.events_btn_24.move(width_factor * 7, width_factor * 24)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_24.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_24.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn25
        first_day = first_day + timedelta(hours=6)
        self.events_btn_25.resize(btn_size, btn_size)
        self.events_btn_25.move(width_factor * 16, width_factor * 12)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_25.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_25.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn26
        first_day = first_day + timedelta(hours=6)
        self.events_btn_26.resize(btn_size, btn_size)
        self.events_btn_26.move(width_factor * 24, width_factor * 6)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_26.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_26.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn27
        first_day = first_day + timedelta(hours=6)
        self.events_btn_27.resize(btn_size, btn_size)
        self.events_btn_27.move(width_factor * 32, width_factor * 3)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_27.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_27.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )
        # btn28
        first_day = first_day + timedelta(hours=6)
        self.events_btn_28.resize(btn_size, btn_size)
        self.events_btn_28.move(width_factor * 40, width_factor * 1)
        events = self.event_manager.events_between(first_day, first_day + timedelta(hours=6))
        self.events_btn_28.setText(
            str(len(events))
        )
        events_content = self.event_manager.events_html(events)
        self.events_btn_28.setToolTip(
            f"""<html><head/><body style="background-color: #aaaaaa;">{events_content}</body></html>"""
        )

    def settings_window(self):
        dialog = SettingsDialog(self, event_manager=self.event_manager, app_settings=self.app_settings)
        return dialog.show()

    def events_window(self, start, end):
        dialog = EventsDialog(
            self, event_manager=self.event_manager, app_settings=self.app_settings,
            start=start, end=end
        )
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

    def make_event_button_action(self, start, end):
        def open_event_window():
            self.events_window(start, end)
        return open_event_window
